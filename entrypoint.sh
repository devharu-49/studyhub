#!/bin/bash
if [ -e /app/uwsgi.sock ]; then
    echo "Removing existing uwsgi.sock (force)..."
    rm -rf /app/uwsgi.sock  # ディレクトリだった場合でも強制削除
fi

# データベースが起動するまで待機
echo "Waiting for database..."
/app/wait-for-it.sh db 3306 -- echo "Database is up"

# マイグレーション実行
echo "Applying database migrations..."
python manage.py migrate --noinput

# 静的ファイルの収集
echo "Collecting static files..."
if ! python manage.py collectstatic --noinput --clear; then
  echo "Collectstatic failed, but continuing..."
fi

# uWSGI 起動
echo "Starting uWSGI..."
exec uwsgi --ini /app/uwsgi.ini
