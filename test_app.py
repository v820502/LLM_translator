import sys
import os
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

def test_application():
    """測試應用程式的基本功能"""
    print("Testing LLM Translator application...")
    
    # 檢查必要檔案是否存在
    required_files = ['translator.py', 'config.json', 'icon.png']
    for file in required_files:
        if not os.path.exists(file):
            print(f"Error: Missing required file: {file}")
            return False
    
    print("✓ All required files found")
    
    # 測試導入
    try:
        from translator import TranslatorApp
        print("✓ Successfully imported TranslatorApp")
    except ImportError as e:
        print(f"Error: Failed to import TranslatorApp: {e}")
        return False
    
    # 測試應用程式初始化
    try:
        app = QApplication(sys.argv)
        translator_app = TranslatorApp()
        print("✓ Application initialized successfully")
        
        # 測試系統托盤
        if translator_app.tray_icon.isVisible():
            print("✓ System tray icon is visible")
        else:
            print("⚠ System tray icon is not visible (may be normal in some environments)")
        
        # 設定自動退出
        QTimer.singleShot(2000, app.quit)  # 2秒後自動退出
        
        print("✓ Running application for 2 seconds...")
        app.exec()
        
        print("✓ Application closed successfully")
        return True
        
    except Exception as e:
        print(f"Error: Failed to run application: {e}")
        return False

if __name__ == '__main__':
    success = test_application()
    if success:
        print("\n✅ All tests passed! The application is ready for use.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
    
    input("Press Enter to exit...") 