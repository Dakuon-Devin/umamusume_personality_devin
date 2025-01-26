from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.models import UserResponse, PersonalityQuizRequest, PersonalityQuizResponse

from app.rag import get_umamusume_result
from app.auth import (
        authenticate_user,
        fake_users_db,
        get_current_user,
        create_access_token,
        User
    )


# FastAPIアプリケーションの初期化
app = FastAPI()


# CORSミドルウェアの追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンからのリクエストを許可 (必要に応じて制限可能)
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのヘッダーを許可
)


@app.get("/")
def read_root():
    return {"message": "Umamusume Personality Quiz is working!"}


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(
        fake_users_db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # JWTトークンを生成
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# 認証されたユーザーの情報を返すエンドポイント
@app.get("/users/me", response_model=UserResponse)  # レスポンスモデルを指定
async def read_users_me(current_user: User = Depends(get_current_user)):
    # パスワードなどの機密情報は含まないUserResponseを返す
    return UserResponse(
        username=current_user.username,
        full_name=current_user.full_name,
        disabled=current_user.disabled
    )


# 性格診断エンドポイント
@app.post("/api/getUmamusume", response_model=PersonalityQuizResponse)
async def get_umamusume_quiz(
    request: PersonalityQuizRequest,
    current_user: User = Depends(get_current_user)
):
    # 質問内容をまとめてRAGに渡す
    input_text = f"私は{request.question1}、{request.question2}です。"
    result = get_umamusume_result(input_text)

    # 診断結果を返す
    return PersonalityQuizResponse(
        name=result.get("name", "不明"),
        personality=result.get("personality", "不明"),
        url=result.get("url", "")
    )
