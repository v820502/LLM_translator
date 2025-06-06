@echo off
chcp 65001 >nul
title LLM翻譯器啟動器

echo ========================================
echo       LLM翻譯器啟動器
echo ========================================
echo.

echo 選擇翻譯器版本:
echo 1. 無GUI版本 (推薦，避免視窗卡住)
echo 2. 完整GUI版本
echo 3. 簡單翻譯測試
echo 4. 退出
echo.

set /p choice="請選擇 (1-4): "

if "%choice%"=="1" goto start_no_gui
if "%choice%"=="2" goto start_full_gui
if "%choice%"=="3" goto start_test
if "%choice%"=="4" goto exit
goto invalid_choice

:start_no_gui
echo.
echo 🚀 啟動無GUI翻譯器...
echo 📋 使用方式：複製文字後按 Ctrl+C 進行翻譯
echo 🔧 更多操作：右鍵點擊系統托盤圖示
echo.
python translator_no_gui.py
goto end

:start_full_gui
echo.
echo 🚀 啟動完整GUI翻譯器...
echo ⚠️  注意：如果遇到視窗卡住，請使用無GUI版本
echo.
python translator.py
goto end

:start_test
echo.
echo 🧪 運行簡單翻譯測試...
echo.
echo 1 | python test_translation_simple.py
echo.
pause
goto end

:invalid_choice
echo.
echo ❌ 無效選擇，請重新選擇
echo.
pause
goto :eof

:exit
echo.
echo 👋 再見！
goto end

:end
echo.
echo 程式已結束
pause 