#!/usr/bin/env bash

TIMEOUT=30
HOST="$1"
PORT="$2"
shift 2
CMD="$@"

echo "Waiting for $HOST:$PORT to be available..."

while ! nc -z "$HOST" "$PORT"; do
  sleep 1
  TIMEOUT=$((TIMEOUT - 1))
  if [ "$TIMEOUT" -le 0 ]; then
    echo "Timeout waiting for $HOST:$PORT"
    exit 1
  fi
done

echo "$HOST:$PORT is available. Running the command..."
exec $CMD  # 修正点
