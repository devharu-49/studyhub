FROM python:3.10-slim

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    libmariadb-dev \
    gcc \
    pkg-config \
    netcat-openbsd \
    curl \
    && apt-get clean

# Node.jsとnpmをインストール（Tailwind CSSの依存関係をインストールするために必要）
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

# 作業ディレクトリの設定
WORKDIR /app

# 依存関係をインストール
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . /app/

# Tailwind CSSインストール
RUN npm install tailwindcss@3.4.17 @tailwindcss/aspect-ratio

# TailwindCSSの初期化。設定ファイルtailwind.config.jsの作成
RUN npx tailwindcss init

# 実行コマンドを指定
CMD ["sh", "-c", "./wait-for-it.sh db:3306 -- python manage.py migrate && python manage.py runserver 0.0.0.0:8000 && npm run watch"]

WORKDIR /app

