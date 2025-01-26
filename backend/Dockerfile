# Pythonの公式イメージを使う
FROM python:3.10-slim

# Poetryのインストール
RUN pip install poetry

# 作業ディレクトリを設定
WORKDIR /app

# Poetryの設定で仮想環境をコンテナの中に作らないようにする
RUN poetry config virtualenvs.create false

# プロジェクトファイルをコンテナにコピー
COPY pyproject.toml poetry.lock ./

# 依存関係のインストール
RUN poetry install --no-root

# アプリケーションのコードをコピー
COPY . .

# FastAPIのアプリケーションを起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
