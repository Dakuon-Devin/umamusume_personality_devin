import os

from dotenv import load_dotenv
from fastapi import HTTPException
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.umamusume_data import umamusume_profiles

# .envファイルから環境変数をロード
load_dotenv()

# OpenAI APIキーを取得
try:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
except KeyError as err:
    raise HTTPException(status_code=500, detail="OpenAI API key is not set.") from err


# ウマ娘のプロフィールデータを使ったRetrieveQAのロジック
def get_umamusume_result(input_text: str):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key is not set.")

    # OpenAI LLMの設定 (RAGの生成部分)
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        openai_api_key=OPENAI_API_KEY,
    )

    try:
        # プロフィール文をドキュメントとして扱う
        docs = [
            Document(
                page_content=profile.get("profile"),
                metadata=profile,
            )
            for profile in umamusume_profiles
        ]

        # OpenAI Embeddingsを使ってドキュメントを埋め込みベクトル化
        embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
        vectorstore = FAISS.from_documents(docs, embeddings)
        retriever = vectorstore.as_retriever()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to set up retriver: {e}") from e

    try:
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",  # 生成部分で関連情報を補完
            retriever=retriever,
            return_source_documents=True,  # 検索に使用されたソースドキュメントを返す
        )
        result = qa_chain.invoke(input_text)
        print(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve answer: {e}") from e

    try:
        # 結果が存在し、ソースドキュメントが空でないことを確認
        if not result or not result["source_documents"]:
            raise HTTPException(
                status_code=500, detail="No source documents found in the result"
            )

        # 一番一致したウマ娘のプロフィールを返す
        best_match = result["source_documents"][0].metadata
        return {
            "name": best_match["name"],
            "personality": best_match["profile"],
            "url": best_match["url"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse result: {e}") from e
