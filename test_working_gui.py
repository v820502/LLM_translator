#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試修復版GUI翻譯器
"""

import pyperclip
import time

def test_working_gui():
    """測試GUI翻譯器功能"""
    print("🧪 測試修復版GUI翻譯器")
    print("=" * 60)
    
    # 測試文字
    test_texts = [
        "Hello world, how are you?",
        "This is a translation test.",
        "Good morning everyone!",
        "Thank you for using this translator.",
        "Python is a great programming language."
    ]
    
    print("📋 測試步驟:")
    print("1. 確保翻譯器正在運行")
    print("2. 檢查系統托盤是否有翻譯器圖示")
    print("3. 依次測試以下文字")
    print("")
    
    for i, text in enumerate(test_texts, 1):
        print(f"📝 測試 {i}/5: {text}")
        print("   步驟:")
        print("   1. 文字已複製到剪貼簿")
        print("   2. 請按 Ctrl+C 觸發翻譯")
        print("   3. 檢查是否有翻譯視窗彈出")
        print("")
        
        # 複製到剪貼簿
        pyperclip.copy(text)
        
        # 等待用戶測試
        input(f"   按 Enter 繼續下一個測試...")
        print("")
    
    print("🎯 額外測試:")
    print("1. 右鍵點擊系統托盤圖示")
    print("2. 選擇 '🧪 測試翻譯' 來直接測試")
    print("3. 選擇 '🔄 翻譯剪貼簿' 來翻譯當前剪貼簿內容")
    print("4. 雙擊托盤圖示應該顯示空的翻譯視窗")
    print("")
    
    print("✅ 測試完成！")
    print("💡 如果視窗沒有顯示，請檢查:")
    print("   - 翻譯器是否正在運行")
    print("   - 控制台是否有錯誤訊息")
    print("   - 系統托盤圖示是否正常")

if __name__ == "__main__":
    test_working_gui() 