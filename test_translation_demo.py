#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
滑鼠高亮翻譯功能演示
"""

import tkinter as tk
from tkinter import scrolledtext
import pyperclip
import time

class TranslationDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("翻譯功能測試 - 請選取文字並按 Ctrl+C")
        self.root.geometry("600x400")
        
        # 創建說明標籤
        instruction = tk.Label(self.root, 
                              text="📋 選取下面任何文字，然後按 Ctrl+C 來測試翻譯功能", 
                              font=("Arial", 12), 
                              fg="blue")
        instruction.pack(pady=10)
        
        # 創建文字區域
        self.text_area = scrolledtext.ScrolledText(self.root, 
                                                  wrap=tk.WORD, 
                                                  font=("Arial", 11),
                                                  height=20)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 插入測試文字
        test_texts = [
            "Hello World - 這是一個簡單的英文句子",
            "Good morning everyone - 早安，各位",
            "Thank you very much for your help - 非常感謝您的幫助",
            "How are you today? - 你今天好嗎？",
            "The weather is beautiful today - 今天天氣很美",
            "I love programming - 我喜歡程式設計",
            "Python is a great programming language - Python是一個很棒的程式語言",
            "",
            "=== 其他語言測試 ===",
            "こんにちは - 日文：你好",
            "안녕하세요 - 韓文：你好", 
            "Bonjour - 法文：你好",
            "Guten Tag - 德文：你好",
            "Hola - 西班牙文：你好",
            "Привет - 俄文：你好",
            "",
            "=== 長句測試 ===",
            "This is a longer sentence that contains multiple words and should be translated properly by the system.",
            "Machine translation has improved significantly with the advancement of artificial intelligence and deep learning technologies.",
        ]
        
        for text in test_texts:
            self.text_area.insert(tk.END, text + "\n\n")
        
        # 創建狀態標籤
        self.status_label = tk.Label(self.root, 
                                    text="✅ 翻譯器已運行。選取文字並按 Ctrl+C 來測試翻譯功能！", 
                                    font=("Arial", 10), 
                                    fg="green")
        self.status_label.pack(pady=5)
        
        # 創建按鈕
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)
        
        test_button = tk.Button(button_frame, 
                               text="🔤 測試剪貼板", 
                               command=self.test_clipboard,
                               font=("Arial", 10))
        test_button.pack(side=tk.LEFT, padx=5)
        
        close_button = tk.Button(button_frame, 
                                text="❌ 關閉", 
                                command=self.root.quit,
                                font=("Arial", 10))
        close_button.pack(side=tk.LEFT, padx=5)
    
    def test_clipboard(self):
        """測試剪貼板功能"""
        try:
            content = pyperclip.paste()
            self.status_label.config(text=f"📋 剪貼板內容: '{content[:50]}{'...' if len(content) > 50 else ''}'", 
                                   fg="blue")
        except Exception as e:
            self.status_label.config(text=f"❌ 剪貼板讀取錯誤: {e}", fg="red")
    
    def run(self):
        """運行演示"""
        self.root.mainloop()

if __name__ == "__main__":
    print("🚀 啟動翻譯功能演示...")
    print("📱 請確保翻譯器應用程序正在運行")
    print("🔤 在打開的視窗中選取文字並按 Ctrl+C")
    print("🎯 應該會在滑鼠附近彈出翻譯結果")
    
    demo = TranslationDemo()
    demo.run() 