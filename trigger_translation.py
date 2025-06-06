#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
觸發翻譯測試
"""

import pyperclip
import time
import keyboard

def trigger_translation_test():
    """觸發翻譯測試"""
    print("🔧 觸發翻譯測試...")
    
    # 測試文本
    test_text = "Hello World"
    
    print(f"📝 準備翻譯文本: {test_text}")
    
    # 複製到剪貼板
    pyperclip.copy(test_text)
    print("✅ 文本已複製到剪貼板")
    
    print("🔥 等待2秒後自動觸發Ctrl+C...")
    time.sleep(2)
    
    try:
        # 模擬 Ctrl+C 按鍵
        keyboard.send('ctrl+c')
        print("⌨️ 已發送 Ctrl+C 按鍵")
        
        print("⏳ 等待5秒觀察翻譯結果...")
        time.sleep(5)
        
        print("✅ 測試完成")
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")

if __name__ == "__main__":
    print("📱 請確保翻譯器應用程序正在運行")
    print("🚀 開始測試...")
    trigger_translation_test() 