#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速Debug工具 - 檢查翻譯器狀態和功能
"""

import psutil
import pyperclip
import time
import json

def quick_status_check():
    """快速狀態檢查"""
    print("🔍 快速狀態檢查...")
    
    # 檢查進程
    translator_running = False
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'python' in proc.info['name'].lower():
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                if 'translator.py' in cmdline:
                    print(f"✅ 翻譯器正在運行 (PID: {proc.info['pid']})")
                    translator_running = True
                    break
        except:
            continue
    
    if not translator_running:
        print("❌ 翻譯器未運行")
        return False
    
    # 檢查配置
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"✅ 配置正常 - 自動翻譯: {config.get('auto_translate', 'unknown')}")
    except Exception as e:
        print(f"❌ 配置錯誤: {e}")
        return False
    
    return True

def test_translation():
    """測試翻譯功能"""
    print("\n🧪 測試翻譯功能...")
    
    test_texts = [
        "Hello world",
        "How are you?",
        "Good morning"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n測試 {i}: {text}")
        
        # 清空剪貼簿
        pyperclip.copy("")
        time.sleep(0.5)
        
        # 放入測試文字
        pyperclip.copy(text)
        print(f"  已放入剪貼簿: {text}")
        
        # 等待翻譯
        print("  等待翻譯結果...")
        time.sleep(3)
        
        # 檢查是否有變化
        current = pyperclip.paste()
        if current == text:
            print("  ⚠️ 剪貼簿內容未變更，可能需要手動觸發翻譯")
        else:
            print(f"  ✅ 偵測到變化: {current}")

def main():
    print("LLM翻譯器 - 快速Debug工具")
    print("=" * 40)
    
    # 狀態檢查
    if not quick_status_check():
        print("\n❌ 程式狀態異常，請檢查")
        return
    
    # 翻譯測試
    test_translation()
    
    print("\n" + "=" * 40)
    print("Debug檢查完成")
    
    # 監控提示
    print("\n💡 提示:")
    print("1. 檢查系統托盤是否有翻譯器圖示")
    print("2. 選擇文字後按 Ctrl+C 應該會觸發翻譯")
    print("3. 如果沒有反應，請檢查熱鍵設定")

if __name__ == "__main__":
    main() 