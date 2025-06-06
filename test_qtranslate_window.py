#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試QTranslate風格翻譯器視窗顯示
"""

import pyperclip
import time

def test_window_display():
    """測試視窗顯示功能"""
    print("🧪 QTranslate風格視窗測試")
    print("=" * 50)
    
    # 測試文字列表
    test_texts = [
        "Hello world",
        "This is a test message",
        "How are you today?",
        "Good morning",
        "Thank you very much"
    ]
    
    print("📋 將測試文字複製到剪貼簿並模擬Ctrl+C...")
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n[測試 {i}/5] 測試文字: {text}")
        
        # 複製到剪貼簿
        pyperclip.copy(text)
        print(f"   ✅ 已複製到剪貼簿")
        
        # 等待用戶按下Ctrl+C進行翻譯
        print(f"   ⌨️  請按 Ctrl+C 進行翻譯，然後觀察視窗是否彈出")
        print(f"   ⏰ 等待5秒後進行下一個測試...")
        
        time.sleep(5)
    
    print("\n" + "=" * 50)
    print("✅ 測試完成！")
    print("💡 如果視窗沒有彈出，請檢查:")
    print("   1. 翻譯器是否正在運行")
    print("   2. 系統托盤是否有翻譯器圖示")
    print("   3. 是否有錯誤訊息")

if __name__ == "__main__":
    test_window_display() 