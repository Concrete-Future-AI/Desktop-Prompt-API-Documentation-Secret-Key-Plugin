#!/bin/bash

# Prompt Manager 一键启动脚本
# 双击即可后台启动应用

# 获取脚本所在目录（支持任意位置）
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$SCRIPT_DIR"
cd "$PROJECT_DIR"

# 日志文件
LOG_FILE="/tmp/prompt_manager.log"

# 检查是否已经在运行
if pgrep -f "main_with_ball.py" > /dev/null; then
    echo "⚠️  Prompt Manager 已在运行"
    echo "如需重启，请先关闭现有进程"
    osascript -e 'display notification "Prompt Manager 已在运行" with title "⚠️ 启动失败"'
    sleep 2
    exit 1
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 未找到虚拟环境"
    echo "请先运行: python3 -m venv venv && venv/bin/pip install -r requirements.txt"
    osascript -e 'display notification "未找到虚拟环境" with title "❌ 启动失败"'
    sleep 3
    exit 1
fi

# 清空旧日志
> "$LOG_FILE"

# 后台启动
echo "🚀 正在启动 Prompt Manager..."
nohup ./venv/bin/python main_with_ball.py > "$LOG_FILE" 2>&1 &

# 等待启动
sleep 2

# 检查是否成功启动
if pgrep -f "main_with_ball.py" > /dev/null; then
    echo "✅ Prompt Manager 启动成功！"
    echo "📍 浮动球应该已显示在屏幕上"
    echo "📋 日志文件: $LOG_FILE"
    osascript -e 'display notification "浮动球已启动，随时可用" with title "✅ 启动成功"'
else
    echo "❌ 启动失败，请查看日志: $LOG_FILE"
    osascript -e 'display notification "请查看日志文件" with title "❌ 启动失败"'
    sleep 3
    exit 1
fi

sleep 2
