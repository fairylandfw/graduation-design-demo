#!/bin/bash

echo "==================================="
echo "网络舆情分析平台 - 快速启动脚本"
echo "==================================="

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未安装Python3"
    exit 1
fi

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "错误: 未安装Node.js"
    exit 1
fi

# 启动后端
echo ""
echo "[1/3] 启动后端服务..."
cd backend
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt -q

echo "后端服务启动中..."
python run.py &
BACKEND_PID=$!
echo "后端PID: $BACKEND_PID"

# 启动前端
echo ""
echo "[2/3] 启动前端服务..."
cd ../frontend
if [ ! -d "node_modules" ]; then
    echo "安装前端依赖..."
    npm install
fi

echo "前端服务启动中..."
npm run serve &
FRONTEND_PID=$!
echo "前端PID: $FRONTEND_PID"

echo ""
echo "[3/3] 服务启动完成!"
echo "==================================="
echo "后端地址: http://localhost:5000"
echo "前端地址: http://localhost:8080"
echo "==================================="
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待中断信号
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
