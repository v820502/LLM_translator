@echo off
echo Starting LLM Translator build process...

REM 檢查 Python 是否已安裝
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

REM 安裝依賴
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

REM 生成圖標
echo Generating icon...
python icon.py
if errorlevel 1 (
    echo Error: Failed to generate icon
    pause
    exit /b 1
)

REM 清理舊的建構檔案
echo Cleaning old build files...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist LLM_Translator.spec del LLM_Translator.spec

REM 使用 PyInstaller 打包
echo Building executable...
python -m PyInstaller --name=LLM_Translator --windowed --noconsole --icon=icon.png --add-data="icon.png;." --add-data="config.json;." --onefile --clean --noconfirm --hidden-import=pkgutil --hidden-import=PyQt5.sip --hidden-import=PyQt5.QtCore --hidden-import=PyQt5.QtWidgets --hidden-import=PyQt5.QtGui --hidden-import=importlib.metadata --hidden-import=googletrans --hidden-import=httpx --hidden-import=httpcore --hidden-import=sqlite3 --hidden-import=hashlib --hidden-import=datetime --hidden-import=typing translator.py

if errorlevel 1 (
    echo Error: Build failed
    pause
    exit /b 1
)

REM 檢查輸出檔案
if exist "dist\LLM_Translator.exe" (
    echo.
    echo Build completed successfully!
    echo Executable created at: dist\LLM_Translator.exe
    echo.
    
    REM 運行測試套件
    echo Running post-build tests...
    python test_build.py
    if errorlevel 1 (
        echo.
        echo ⚠️ Warning: Some tests failed! Please check the test output above.
        echo The executable was built but may have issues.
        echo.
    ) else (
        echo.
        echo ✅ All tests passed! The build is verified and ready to use.
        echo.
    )
    
    echo To test the application manually:
    echo 1. Run dist\LLM_Translator.exe
    echo 2. Check if the icon appears in the system tray
    echo 3. Select some text and press Ctrl+C to test translation
    echo.
) else (
    echo Error: Executable was not created!
)

pause 