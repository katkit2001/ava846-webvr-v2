#!/bin/bash

cd "$(dirname "$0")" || exit 1

PORT=8000
while lsof -i ":$PORT" >/dev/null 2>&1; do PORT=$((PORT + 1)); done
python3 -m http.server "$PORT" &
SERVER=$!
trap 'kill "$SERVER" 2>/dev/null' EXIT

for _ in $(seq 1 50); do
  if curl -s -o /dev/null "http://localhost:$PORT/"; then break; fi
  sleep 0.1
done

open "http://localhost:$PORT/"
echo "Server: http://localhost:$PORT/   —  Ctrl+C για τερματισμό."
wait "$SERVER"
