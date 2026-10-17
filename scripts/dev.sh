#!/bin/bash
docker compose up -d

# DB が起動するまで待つ（たぶん 5 秒あれば大丈夫）
sleep 5

(cd api && uv run uvicorn main:app --port 8000) &
(cd frontend && npm run dev) &

wait
