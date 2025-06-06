#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試滑鼠高亮翻譯功能
"""

import sys
import time
import pyperclip

def test_highlight_translation():
    """測試滑鼠高亮翻譯功能"""
    print("🔧 測試滑鼠高亮翻譯功能...")
    print("📱 確保翻譯應用程序正在運行")
    
    # 測試文本
    test_texts = [
        "Hello World",
        "Good morning",  
        "Thank you very much",
        "How are you today?",
        "こんにちは",  # 日文
        "안녕하세요",   # 韓文
        "Bonjour"      # 法文
    ]
    
    print("\n📝 測試說明：")
    print("1. 打開任何文本編輯器（如記事本）")
    print("2. 複製以下測試文本")
    print("3. 選中文本並按 Ctrl+C")
    print("4. 查看是否出現翻譯彈窗")
    print("=" * 50)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n🔤 測試 {i}: {text}")
        
        # 將文本複製到剪貼板
        pyperclip.copy(text)
        print(f"✅ 已複製到剪貼板: {text}")
        
        print("📋 現在選中此文本並按 Ctrl+C 測試翻譯功能")
        print("   (應該會彈出翻譯視窗)")
        
        # 等待用戶測試
        input("按 Enter 繼續下一個測試...")
    
    print("\n🏁 測試完成！")
    print("如果翻譯彈窗沒有出現，可能的原因：")
    print("1. 鍵盤監聽沒有啟動")
    print("2. 翻譯服務配置有問題") 
    print("3. 需要管理員權限來監聽全局快捷鍵")

def check_clipboard_content():
    """檢查剪貼板內容"""
    print("\n🔍 檢查剪貼板內容...")
    try:
        content = pyperclip.paste()
        print(f"📋 剪貼板內容: '{content}'")
        print(f"📏 內容長度: {len(content)}")
        return content
    except Exception as e:
        print(f"❌ 讀取剪貼板失敗: {e}")
        return None

if __name__ == "__main__":
    # 檢查剪貼板功能
    check_clipboard_content()
    
    # 運行測試
    test_highlight_translation() 