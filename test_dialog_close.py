#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試對話框關閉不會導致應用程序退出
"""

import sys
import os
import time
import subprocess

def test_dialog_close():
    """測試對話框關閉行為"""
    print("🔧 測試對話框關閉行為...")
    
    # 啟動應用程序
    process = subprocess.Popen([sys.executable, "translator.py"], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
    
    print(f"📱 應用程序已啟動 (PID: {process.pid})")
    
    # 等待應用程序初始化
    time.sleep(3)
    
    # 檢查進程是否還在運行
    if process.poll() is None:
        print("✅ 應用程序成功啟動")
    else:
        print("❌ 應用程序啟動失敗")
        return False
    
    print("📝 說明：")
    print("1. 右鍵點擊系統托盤圖標")
    print("2. 選擇 '設置' 菜單項")
    print("3. 關閉設置對話框")
    print("4. 檢查應用程序是否仍在運行")
    print("5. 按 Ctrl+C 停止測試")
    
    try:
        # 等待用戶測試
        while True:
            if process.poll() is not None:
                print("❌ 應用程序意外退出！")
                return False
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 測試停止")
        
        # 檢查應用程序是否還在運行
        if process.poll() is None:
            print("✅ 應用程序仍在運行，對話框關閉測試通過！")
            # 終止應用程序
            process.terminate()
            process.wait()
            return True
        else:
            print("❌ 應用程序已退出，對話框關閉測試失敗！")
            return False

if __name__ == "__main__":
    success = test_dialog_close()
    sys.exit(0 if success else 1) 