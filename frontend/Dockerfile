# Node.jsの公式イメージを使用
FROM node:18

# 作業ディレクトリを設定
WORKDIR /app

# package.jsonと依存関係のインストール
COPY package.json yarn.lock ./
RUN yarn install

# アプリケーションのコードをコピー
COPY . .

# Reactアプリをビルド
RUN yarn build

# 静的ファイルを提供するために使用する
CMD ["yarn", "start"]
