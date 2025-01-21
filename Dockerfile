FROM python:3.10-slim

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    libmariadb-dev \
    gcc \
    pkg-config \
    netcat-openbsd \
    && apt-get clean

# 作業ディレクトリの設定
WORKDIR /app

# 依存関係をインストール
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . /app/

# 実行コマンドを指定
CMD ["sh", "-c", "./wait-for-it.sh db:3306 -- python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

WORKDIR /app
