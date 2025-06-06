#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完全修復版翻譯器 - 解決視窗顯示問題
專注於確保視窗能夠正常顯示和響應
"""

import sys
import os
import pyperclip
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, 
                           QVBoxLayout, QHBoxLayout, QTextEdit, 
                           QSystemTrayIcon, QMenu, QAction)
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer, Qt
from PyQt5.QtGui import QIcon
import keyboard

class TranslationWorker(QThread):
    """翻譯工作線程"""
    translation_complete = pyqtSignal(str, str)  # original, translation
    
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
            
            self.translation_complete.emit(self.text, translation)
            
        except Exception as e:
            print(f"[ERROR] ❌ 翻譯失敗: {e}")
            self.translation_complete.emit(self.text, f"翻譯失敗: {str(e)}")

class TranslationWindow(QWidget):
    """翻譯顯示視窗"""
    
    def __init__(self):
        super().__init__()
        self.current_translation = ""
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        # 設置視窗屬性
        self.setWindowTitle("🔤 LLM翻譯器")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Window)  # 使用Window而不是Tool
        self.setFixedSize(500, 350)
        
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
        self.source_text.setMaximumHeight(70)
        self.source_text.setReadOnly(True)
        self.source_text.setStyleSheet("""
            QTextEdit {
                border: 2px solid #0078d4;
                border-radius: 6px;
                padding: 10px;
                background-color: #f8f9fa;
                font-size: 12px;
                color: #333;
            }
        """)
        layout.addWidget(self.source_text)
        
        # 翻譯結果區域
        result_label = QLabel("🌍 翻譯結果:")
        result_label.setStyleSheet("font-weight: bold; color: #333; font-size: 12px;")
        layout.addWidget(result_label)
        
        self.result_text = QTextEdit()
        self.result_text.setMaximumHeight(90)
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet("""
            QTextEdit {
                border: 2px solid #28a745;
                border-radius: 6px;
                padding: 10px;
                background-color: white;
                font-size: 12px;
                color: #333;
                font-weight: bold;
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
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        keep_btn = QPushButton("📌 保持顯示")
        keep_btn.clicked.connect(self.keep_window_open)
        keep_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 20px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #106ebe;
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
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        
        button_layout.addWidget(copy_btn)
        button_layout.addWidget(keep_btn)
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
    
    def show_translation(self, original_text, translation):
        """顯示翻譯結果"""
        try:
            print(f"[DEBUG] 📋 準備顯示翻譯視窗")
            print(f"[DEBUG] 原文: {original_text[:50]}...")
            print(f"[DEBUG] 翻譯: {translation[:50]}...")
            
            # 設置文字
            self.source_text.setPlainText(original_text)
            self.result_text.setPlainText(translation)
            self.current_translation = translation
            
            # 自動複製到剪貼簿
            try:
                pyperclip.copy(translation)
                print(f"[SUCCESS] 📋 已自動複製到剪貼簿")
            except Exception as e:
                print(f"[WARNING] ⚠️ 自動複製失敗: {e}")
            
            # 計算視窗位置（螢幕中央偏右）
            screen = QApplication.desktop().screenGeometry()
            x = (screen.width() - self.width()) // 2 + 100
            y = (screen.height() - self.height()) // 2
            self.move(x, y)
            
            # 顯示視窗
            print(f"[DEBUG] 🪟 正在顯示視窗...")
            self.show()
            self.raise_()
            self.activateWindow()
            
            print(f"[SUCCESS] ✅ 翻譯視窗已顯示並置頂！")
            
            # 使用QApplication的單次定時器，15秒後自動關閉
            QTimer.singleShot(15000, self.auto_close)
            
        except Exception as e:
            print(f"[ERROR] ❌ 顯示視窗失敗: {e}")
            import traceback
            traceback.print_exc()
    
    def copy_translation(self):
        """複製翻譯結果"""
        if self.current_translation:
            try:
                pyperclip.copy(self.current_translation)
                print(f"[SUCCESS] 📋 手動複製完成")
                # 顯示複製成功提示
                self.result_text.setPlainText(f"{self.current_translation}\n\n✅ 已複製到剪貼簿！")
            except Exception as e:
                print(f"[ERROR] ❌ 複製失敗: {e}")
    
    def keep_window_open(self):
        """保持視窗開啟"""
        print(f"[INFO] 📌 視窗將保持開啟")
        # 取消自動關閉
    
    def auto_close(self):
        """自動關閉"""
        print(f"[INFO] ⏰ 視窗自動關閉")
        self.hide()
    
    def close_window(self):
        """關閉視窗"""
        print(f"[INFO] ❌ 手動關閉視窗")
        self.hide()

class WorkingTranslator(QObject):
    """工作正常的翻譯器"""
    
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        # 創建翻譯視窗
        self.translation_window = TranslationWindow()
        
        # 設置系統托盤
        self.setup_tray()
        
        # 剪貼簿監控
        self.last_clipboard_text = ""
        
        print("[INFO] ✅ 翻譯器初始化完成")
    
    def setup_tray(self):
        """設置系統托盤"""
        try:
            # 創建托盤圖示
            icon = self.app.style().standardIcon(self.app.style().SP_ComputerIcon)
            self.tray_icon = QSystemTrayIcon(icon)
            
            # 創建托盤菜單 - 修復參數問題
            tray_menu = QMenu()
            
            # 添加菜單項
            status_action = QAction("🔤 LLM翻譯器")
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
            import traceback
            traceback.print_exc()
    
    def setup_hotkeys(self):
        """設置熱鍵"""
        try:
            print("[INFO] 🔑 註冊Ctrl+C熱鍵...")
            keyboard.add_hotkey('ctrl+c', self.on_hotkey_pressed, suppress=False)
            print("[SUCCESS] ✅ 熱鍵註冊成功")
        except Exception as e:
            print(f"[WARNING] ⚠️ 熱鍵註冊失敗: {e}")
    
    def on_hotkey_pressed(self):
        """熱鍵按下事件 - 避免線程問題"""
        try:
            print(f"[DEBUG] 🔑 Ctrl+C 被按下")
            # 使用QApplication的單次定時器避免線程問題
            QTimer.singleShot(300, self.check_and_translate_clipboard)
        except Exception as e:
            print(f"[ERROR] ❌ 熱鍵處理錯誤: {e}")
    
    def check_and_translate_clipboard(self):
        """檢查並翻譯剪貼簿內容"""
        try:
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
            print(f"[ERROR] ❌ 剪貼簿檢查錯誤: {e}")
            import traceback
            traceback.print_exc()
    
    def start_translation(self, text):
        """啟動翻譯"""
        try:
            print(f"[INFO] 🚀 啟動翻譯工作線程...")
            self.translation_worker = TranslationWorker(text)
            self.translation_worker.translation_complete.connect(self.on_translation_complete)
            self.translation_worker.start()
        except Exception as e:
            print(f"[ERROR] ❌ 啟動翻譯失敗: {e}")
    
    def on_translation_complete(self, original, translation):
        """翻譯完成回調"""
        try:
            print(f"[SUCCESS] 🎉 翻譯完成，顯示視窗")
            print(f"[DEBUG] 原文: {original[:30]}...")
            print(f"[DEBUG] 翻譯: {translation[:30]}...")
            
            # 確保在主線程中顯示視窗
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
        test_text = "Hello, this is a test message for checking if the translation window displays correctly."
        self.start_translation(test_text)
    
    def manual_translate(self):
        """手動翻譯剪貼簿"""
        print(f"[INFO] 🔄 手動翻譯剪貼簿內容")
        self.check_and_translate_clipboard()
    
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
            print("[INFO] 🚀 啟動翻譯器...")
            
            # 設置熱鍵
            self.setup_hotkeys()
            
            print("[SUCCESS] 🎉 翻譯器已成功啟動！")
            print("=" * 60)
            print("📋 按 Ctrl+C 進行翻譯")
            print("🖱️  右鍵點擊系統托盤圖示查看菜單")
            print("🖱️  雙擊托盤圖示顯示翻譯視窗")
            print("🧪 右鍵選擇'測試翻譯'來測試功能")
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
        translator = WorkingTranslator()
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