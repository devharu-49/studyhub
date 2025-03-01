# ベースイメージ
FROM python:3.11

# 作業ディレクトリを指定
WORKDIR /app

# 必要なシステムパッケージをインストール
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    default-libmysqlclient-dev \
    curl \
    netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 環境変数の設定
ENV PYTHONUNBUFFERED=1

# Node.js をインストール (Tailwind CSS 用)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# 依存関係のインストール
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip  # ✅  Pythonのキャッシュ削除

# Tailwind CSS のインストール
COPY package.json package-lock.json /app/
RUN npm ci

# アプリケーションコードをコピー
COPY . /app/

# Tailwind CSS をビルド
RUN npx tailwindcss -i /app/static/css/tailwind.css -o /app/static/css/style.css --minify

# 静的ファイルを収集
RUN python manage.py collectstatic --noinput

# wait-for-it.sh を追加
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# uWSGI の設定ファイルをコピー
COPY ./uwsgi.ini /app/uwsgi.ini
