@echo off
title 诗词接龙助手启动器
color 0A

echo ====================================
echo         诗词接龙助手启动器
echo ====================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python
    echo 按任意键退出...
    pause >nul
    exit
)

:: 检查必要文件
if not exist poetry_bot.py (
    echo [错误] 未找到 poetry_bot.py 文件
    echo 按任意键退出...
    pause >nul
    exit
)

if not exist static\poems.js (
    echo [错误] 未找到 static\poems.js 文件
    echo 按任意键退出...
    pause >nul
    exit
)

:: 检查并安装必要的库
echo 正在检查必要的Python库...
pip install pyperclip keyboard pywin32 -q

echo.
echo [信息] 正在启动诗词接龙助手...
echo.

:: 启动主程序
python poetry_bot.py

if errorlevel 1 (
    echo.
    echo [错误] 程序运行出错
    echo 按任意键退出...
    pause >nul
) else (
    echo.
    echo [信息] 程序已关闭
    echo 按任意键退出...
    pause >nul
) 