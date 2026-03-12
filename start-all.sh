#!/usr/bin/env bash
# 一键启动三端：用户前端(3000) + 管理后台(3001) + API(8000)
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

API_PID=""
ADMIN_PID=""
FRONT_PID=""

cleanup() {
  echo ""
  echo "正在停止所有服务..."
  for pid in $API_PID $ADMIN_PID $FRONT_PID; do
    [ -n "$pid" ] && kill "$pid" 2>/dev/null || true
  done
  exit 0
}
trap cleanup SIGINT SIGTERM

if ! command -v deno &>/dev/null; then
  echo "未找到 deno，请先安装: https://deno.land"
  exit 1
fi

echo "=========================================="
echo "  心植 · 三端本地开发"
echo "  用户端 http://localhost:3000"
echo "  管理后台 http://localhost:3001"
echo "  API http://localhost:8000"
echo "  按 Ctrl+C 停止全部"
echo "=========================================="
echo ""

echo "[1/3] 启动 API (port 8000)..."
(cd heart-plant-api && deno task serve) &
API_PID=$!
sleep 1

echo "[2/3] 启动管理后台 (port 3001)..."
(cd heart-plant-admin && npm run dev) &
ADMIN_PID=$!
sleep 1

echo "[3/3] 启动用户前端 (port 3000)..."
(cd heart-plant && npm run dev) &
FRONT_PID=$!

echo ""
echo "全部已启动。"
wait
