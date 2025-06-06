#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡單翻譯測試 - 直接測試翻譯功能並返回結果到剪貼簿
"""

import sys
import pyperclip
import time

def simple_google_translate(text, target_lang='zh-tw'):
    """簡單的Google翻譯函數"""
    try:
        from googletrans import Translator
        translator = Translator()
        
        result = translator.translate(text, dest=target_lang)
        return result.text
    except Exception as e:
        print(f"翻譯錯誤: {e}")
        return None

def test_translation_with_clipboard():
    """測試翻譯並將結果放入剪貼簿"""
    print("簡單翻譯測試")
    print("=" * 30)
    
    # 測試案例
    test_cases = [
        "Hello world",
        "How are you today?",
        "Good morning, have a nice day!",
        "The weather is beautiful",
        "I love programming"
    ]
    
    success_count = 0
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n測試 {i}: {text}")
        
        # 執行翻譯
        translation = simple_google_translate(text)
        
        if translation:
            print(f"翻譯結果: {translation}")
            
            # 放入剪貼簿
            combined_result = f"原文: {text}\n翻譯: {translation}"
            pyperclip.copy(combined_result)
            
            print("✅ 翻譯成功，結果已複製到剪貼簿")
            success_count += 1
            
        else:
            print("❌ 翻譯失敗")
        
        time.sleep(1)  # 避免API請求過快
    
    print(f"\n所有測試完成! 成功: {success_count}/{len(test_cases)}")
    
    # 最後一次測試，檢查剪貼簿內容
    print("\n檢查剪貼簿內容:")
    try:
        clipboard_content = pyperclip.paste()
        print(f"剪貼簿內容: {clipboard_content}")
    except Exception as e:
        print(f"無法讀取剪貼簿: {e}")

def interactive_translation():
    """互動式翻譯模式"""
    print("\n互動式翻譯模式")
    print("輸入文字進行翻譯，輸入'quit'退出")
    print("-" * 30)
    
    try:
        while True:
            text = input("\n請輸入要翻譯的文字: ").strip()
            
            if text.lower() in ['quit', 'exit', '退出']:
                break
            
            if not text:
                continue
            
            print("翻譯中...")
            translation = simple_google_translate(text)
            
            if translation:
                print(f"翻譯結果: {translation}")
                
                # 複製到剪貼簿
                combined_result = f"原文: {text}\n翻譯: {translation}"
                pyperclip.copy(combined_result)
                print("✅ 結果已複製到剪貼簿")
            else:
                print("❌ 翻譯失敗")
    except (EOFError, KeyboardInterrupt):
        print("\n程式結束")

def single_test(text="Hello world"):
    """單次翻譯測試"""
    print(f"單次翻譯測試: {text}")
    print("-" * 30)
    
    translation = simple_google_translate(text)
    
    if translation:
        print(f"原文: {text}")
        print(f"翻譯: {translation}")
        
        # 複製到剪貼簿
        pyperclip.copy(translation)
        print("✅ 翻譯結果已複製到剪貼簿")
        return True
    else:
        print("❌ 翻譯失敗")
        return False

def main():
    """主函數"""
    if len(sys.argv) > 1:
        # 如果有命令行參數，執行單次測試
        text = " ".join(sys.argv[1:])
        single_test(text)
        return
    
    print("選擇模式:")
    print("1. 自動測試模式")
    print("2. 互動式翻譯模式")
    print("3. 單次快速測試")
    
    try:
        choice = input("請選擇 (1, 2 或 3): ").strip()
    except (EOFError, KeyboardInterrupt):
        choice = "1"  # 默認自動測試
        print("1")
    
    if choice == "1":
        test_translation_with_clipboard()
    elif choice == "2":
        interactive_translation()
    elif choice == "3":
        single_test()
    else:
        print("無效選擇，執行自動測試...")
        test_translation_with_clipboard()

if __name__ == "__main__":
    main() 