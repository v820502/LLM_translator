#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最終版翻譯器 - 完全解決視窗顯示問題
- 避免QTimer線程錯誤
- 自適應視窗大小
- 簡化架構
- 確保視窗正常顯示
"""

import sys
import os
import pyperclip
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, 
                           QVBoxLayout, QHBoxLayout, QTextEdit, 
                           QSystemTrayIcon, QMenu, QAction, QSizePolicy)
from PyQt5.QtCore import QObject, QThread, pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QIcon, QFont
import keyboard
import time

class SimpleTranslationWorker(QThread):
    """簡化翻譯工作線程"""
    finished = pyqtSignal(str, str)  # original, translation
    
    def __init__(self, text):
        super().__init__()
        self.text = text
    
    def run(self):
        try:
            print(f"[INFO] 🔄 開始翻譯: {self.text[:30]}...")
            
            from googletrans import Translator
            translator = Translator()
            
            result = translator.translate(self.text, src='auto', dest='zh-tw')
            translation = result.text
            
            print(f"[SUCCESS] ✅ 翻譯完成: {translation[:50]}...")
            
            self.finished.emit(self.text, translation)
            
        except Exception as e:
            print(f"[ERROR] ❌ 翻譯失敗: {e}")
            self.finished.emit(self.text, f"翻譯失敗: {str(e)}")

class AdaptiveTranslationWindow(QWidget):
    """自適應翻譯視窗"""
    
    def __init__(self):
        super().__init__()
        self.current_translation = ""
        self.init_ui()
        
    def init_ui(self):
        """初始化自適應UI"""
        # 設置視窗屬性
        self.setWindowTitle("🔤 LLM翻譯器")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Window)
        
        # 主佈局
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 標題
        title = QLabel("🔤 LLM翻譯器")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #0078d4;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 8px;
                border: 2px solid #0078d4;
            }
        """)
        layout.addWidget(title)
        
        # 原文區域
        source_label = QLabel("📝 原文:")
        source_label.setStyleSheet("font-weight: bold; color: #333; font-size: 12px;")
        layout.addWidget(source_label)
        
        self.source_text = QTextEdit()
        self.source_text.setReadOnly(True)
        self.source_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        self.source_text.setStyleSheet("""
            QTextEdit {
                border: 2px solid #0078d4;
                border-radius: 6px;
                padding: 10px;
                background-color: #f8f9fa;
                font-size: 12px;
                color: #333;
                min-height: 60px;
                max-height: 120px;
            }
        """)
        layout.addWidget(self.source_text)
        
        # 翻譯結果區域
        result_label = QLabel("🌍 翻譯結果:")
        result_label.setStyleSheet("font-weight: bold; color: #333; font-size: 12px;")
        layout.addWidget(result_label)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        self.result_text.setStyleSheet("""
            QTextEdit {
                border: 2px solid #28a745;
                border-radius: 6px;
                padding: 10px;
                background-color: white;
                font-size: 13px;
                color: #333;
                font-weight: bold;
                min-height: 80px;
                max-height: 150px;
            }
        """)
        layout.addWidget(self.result_text)
        
        # 按鈕區域
        button_layout = QHBoxLayout()
        
        copy_btn = QPushButton("📋 複製結果")
        copy_btn.clicked.connect(self.copy_translation)
        copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 20px;
                font-weight: bold;
                font-size: 12px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        close_btn = QPushButton("❌ 關閉")
        close_btn.clicked.connect(self.close_window)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 20px;
                font-weight: bold;
                font-size: 12px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        
        button_layout.addWidget(copy_btn)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # 設置整體樣式
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                font-family: 'Microsoft YaHei UI', 'Segoe UI', Arial;
            }
        """)
        
        # 設置最小尺寸
        self.setMinimumSize(400, 300)
    
    def show_translation(self, original_text, translation):
        """顯示翻譯結果並自適應大小"""
        try:
            print(f"[INFO] 📋 準備顯示翻譯視窗")
            
            # 設置文字
            self.source_text.setPlainText(original_text)
            self.result_text.setPlainText(translation)
            self.current_translation = translation
            
            # 自動調整文本框高度
            self.adjust_text_heights(original_text, translation)
            
            # 自動複製到剪貼簿
            try:
                pyperclip.copy(translation)
                print(f"[SUCCESS] 📋 已自動複製到剪貼簿")
            except Exception as e:
                print(f"[WARNING] ⚠️ 自動複製失敗: {e}")
            
            # 調整視窗大小以適應內容
            self.adjustSize()
            
            # 計算視窗位置（螢幕中央）
            screen = QApplication.desktop().screenGeometry()
            x = (screen.width() - self.width()) // 2
            y = (screen.height() - self.height()) // 2
            self.move(x, y)
            
            # 顯示視窗
            print(f"[INFO] 🪟 正在顯示視窗...")
            self.show()
            self.raise_()
            self.activateWindow()
            
            print(f"[SUCCESS] ✅ 翻譯視窗已顯示！")
            
        except Exception as e:
            print(f"[ERROR] ❌ 顯示視窗失敗: {e}")
            import traceback
            traceback.print_exc()
    
    def adjust_text_heights(self, original_text, translation):
        """根據文字內容調整文本框高度"""
        try:
            # 計算原文所需高度
            source_lines = len(original_text.split('\n'))
            source_height = max(60, min(120, source_lines * 20 + 20))
            self.source_text.setMaximumHeight(source_height)
            
            # 計算翻譯結果所需高度
            result_lines = len(translation.split('\n'))
            result_height = max(80, min(150, result_lines * 20 + 20))
            self.result_text.setMaximumHeight(result_height)
            
        except Exception as e:
            print(f"[WARNING] 調整高度失敗: {e}")
    
    def copy_translation(self):
        """複製翻譯結果"""
        if self.current_translation:
            try:
                pyperclip.copy(self.current_translation)
                print(f"[SUCCESS] 📋 手動複製完成")
                # 顯示複製成功提示
                original_text = self.result_text.toPlainText()
                self.result_text.setPlainText(f"{original_text}\n\n✅ 已複製到剪貼簿！")
            except Exception as e:
                print(f"[ERROR] ❌ 複製失敗: {e}")
    
    def close_window(self):
        """關閉視窗"""
        print(f"[INFO] ❌ 關閉視窗")
        self.hide()

class FinalTranslator(QObject):
    """最終版翻譯器"""
    
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        # 創建翻譯視窗
        self.translation_window = AdaptiveTranslationWindow()
        
        # 設置系統托盤
        self.setup_tray()
        
        # 剪貼簿監控
        self.last_clipboard_text = ""
        
        print("[INFO] ✅ 最終版翻譯器初始化完成")
    
    def setup_tray(self):
        """設置系統托盤"""
        try:
            # 創建托盤圖示
            icon = self.app.style().standardIcon(self.app.style().SP_ComputerIcon)
            self.tray_icon = QSystemTrayIcon(icon)
            
            # 創建托盤菜單
            tray_menu = QMenu()
            
            # 添加菜單項
            status_action = QAction("🔤 LLM翻譯器 (最終版)")
            status_action.setEnabled(False)
            tray_menu.addAction(status_action)
            
            tray_menu.addSeparator()
            
            show_action = QAction("🪟 顯示翻譯視窗")
            show_action.triggered.connect(self.show_translation_window)
            tray_menu.addAction(show_action)
            
            test_action = QAction("🧪 測試翻譯")
            test_action.triggered.connect(self.test_translation)
            tray_menu.addAction(test_action)
            
            translate_action = QAction("🔄 翻譯剪貼簿")
            translate_action.triggered.connect(self.manual_translate)
            tray_menu.addAction(translate_action)
            
            tray_menu.addSeparator()
            
            quit_action = QAction("❌ 退出")
            quit_action.triggered.connect(self.quit_app)
            tray_menu.addAction(quit_action)
            
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.show()
            
            # 托盤圖示點擊事件
            self.tray_icon.activated.connect(self.tray_icon_activated)
            
            print("[SUCCESS] ✅ 系統托盤設置完成")
            
        except Exception as e:
            print(f"[ERROR] ❌ 托盤設置失敗: {e}")
    
    def setup_hotkeys(self):
        """設置熱鍵"""
        try:
            print("[INFO] 🔑 註冊Ctrl+C熱鍵...")
            keyboard.add_hotkey('ctrl+c', self.on_hotkey_pressed, suppress=False)
            print("[SUCCESS] ✅ 熱鍵註冊成功")
        except Exception as e:
            print(f"[WARNING] ⚠️ 熱鍵註冊失敗: {e}")
    
    def on_hotkey_pressed(self):
        """熱鍵按下事件 - 直接處理，避免定時器問題"""
        try:
            print(f"[DEBUG] 🔑 Ctrl+C 被按下")
            # 直接處理，不使用QTimer
            self.process_clipboard()
        except Exception as e:
            print(f"[ERROR] ❌ 熱鍵處理錯誤: {e}")
    
    def process_clipboard(self):
        """處理剪貼簿內容 - 避免線程問題"""
        try:
            # 短暫延遲讓剪貼簿更新
            time.sleep(0.1)
            
            text = pyperclip.paste().strip()
            
            print(f"[DEBUG] 📋 剪貼簿內容: {text[:50]}...")
            
            if not text:
                print("[INFO] ℹ️ 剪貼簿為空")
                return
            
            if text == self.last_clipboard_text:
                print("[INFO] ℹ️ 剪貼簿內容未變化")
                return
            
            # 過濾不需要翻譯的內容
            if self.should_skip_translation(text):
                print(f"[INFO] ⏭️ 跳過翻譯: {text[:30]}...")
                return
            
            self.last_clipboard_text = text
            
            print(f"[INFO] 🔄 檢測到新文字，開始翻譯...")
            
            # 啟動翻譯
            self.start_translation(text)
            
        except Exception as e:
            print(f"[ERROR] ❌ 剪貼簿處理錯誤: {e}")
    
    def start_translation(self, text):
        """啟動翻譯"""
        try:
            print(f"[INFO] 🚀 啟動翻譯工作線程...")
            self.translation_worker = SimpleTranslationWorker(text)
            self.translation_worker.finished.connect(self.on_translation_finished)
            self.translation_worker.start()
        except Exception as e:
            print(f"[ERROR] ❌ 啟動翻譯失敗: {e}")
    
    def on_translation_finished(self, original, translation):
        """翻譯完成回調"""
        try:
            print(f"[SUCCESS] 🎉 翻譯完成，顯示視窗")
            
            # 直接在主線程中顯示視窗
            self.translation_window.show_translation(original, translation)
            
        except Exception as e:
            print(f"[ERROR] ❌ 顯示翻譯視窗失敗: {e}")
            import traceback
            traceback.print_exc()
    
    def should_skip_translation(self, text):
        """判斷是否跳過翻譯"""
        # 跳過純數字
        if text.isdigit():
            return True
        # 跳過太短的文本
        if len(text.strip()) < 3:
            return True
        # 跳過URL
        if text.startswith(('http://', 'https://', 'ftp://', 'www.')):
            return True
        # 跳過文件路徑
        if '\\' in text and ':' in text:
            return True
        if text.startswith('/'):
            return True
        return False
    
    def show_translation_window(self):
        """手動顯示翻譯視窗"""
        print(f"[INFO] 🪟 手動顯示翻譯視窗")
        self.translation_window.show()
        self.translation_window.raise_()
        self.translation_window.activateWindow()
    
    def test_translation(self):
        """測試翻譯功能"""
        print(f"[INFO] 🧪 執行測試翻譯")
        test_text = "Hello, this is a comprehensive test message to check if the translation window displays correctly with adaptive sizing."
        self.start_translation(test_text)
    
    def manual_translate(self):
        """手動翻譯剪貼簿"""
        print(f"[INFO] 🔄 手動翻譯剪貼簿內容")
        self.process_clipboard()
    
    def tray_icon_activated(self, reason):
        """托盤圖示激活事件"""
        if reason == QSystemTrayIcon.DoubleClick:
            print(f"[INFO] 🖱️ 雙擊托盤圖示")
            self.show_translation_window()
    
    def quit_app(self):
        """退出應用"""
        print("[INFO] 👋 翻譯器正在退出...")
        try:
            keyboard.unhook_all()
            print("[INFO] ✅ 熱鍵已取消註冊")
        except Exception as e:
            print(f"[WARNING] ⚠️ 熱鍵取消失敗: {e}")
        
        self.app.quit()
    
    def run(self):
        """運行翻譯器"""
        try:
            print("[INFO] 🚀 啟動最終版翻譯器...")
            
            # 設置熱鍵
            self.setup_hotkeys()
            
            print("[SUCCESS] 🎉 最終版翻譯器已成功啟動！")
            print("=" * 60)
            print("📋 按 Ctrl+C 進行翻譯")
            print("🖱️  右鍵點擊系統托盤圖示查看菜單")
            print("🖱️  雙擊托盤圖示顯示翻譯視窗")
            print("🧪 右鍵選擇'測試翻譯'來測試功能")
            print("✨ 視窗大小會自動適應內容")
            print("=" * 60)
            
            return self.app.exec_()
            
        except Exception as e:
            print(f"[ERROR] ❌ 運行錯誤: {e}")
            import traceback
            traceback.print_exc()
            return 1

def main():
    """主函數"""
    try:
        translator = FinalTranslator()
        return translator.run()
    except KeyboardInterrupt:
        print("\n[INFO] 👋 收到中斷信號，退出程式")
        return 0
    except Exception as e:
        print(f"[ERROR] ❌ 程式錯誤: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 