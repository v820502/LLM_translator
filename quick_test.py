#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速測試翻譯功能
"""

import pyperclip
import time

def test_translation():
    """測試翻譯功能"""
    print("🔧 快速測試翻譯功能...")
    
    # 測試文本
    test_text = "Hello World"
    
    print(f"📝 測試文本: {test_text}")
    
    # 複製到剪貼板
    pyperclip.copy(test_text)
    print("✅ 已複製到剪貼板")
    
    print("📋 現在按 Ctrl+C 來觸發翻譯...")
    print("🎯 應該會彈出翻譯視窗在滑鼠位置")
    print("⏱️ 等待 10 秒...")
    
    # 等待用戶測試
    time.sleep(10)
    
    print("✅ 測試完成")

if __name__ == "__main__":
    test_translation() 