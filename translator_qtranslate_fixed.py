#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM翻譯器 - QTranslate風格GUI版本 (修復版)
修復視窗顯示和系統托盤問題
"""

import sys
import os
import json
import time
import pyperclip
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, 
                           QVBoxLayout, QHBoxLayout, QSystemTrayIcon, QMenu, QAction,
                           QTextEdit, QComboBox, QFrame, QProgressBar)
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer, Qt
from PyQt5.QtGui import QIcon, QFont
import keyboard

def resource_path(relative_path):
    """獲取資源文件路徑"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class QTranslateThemes:
    """QTranslate主題系統"""
    
    MODERN_BLUE_THEME = {
        "name": "Modern Blue",
        "window_bg": "#f8f9fa",
        "window_border": "#0078d4",
        "button_normal": "#e1e1e1",
        "button_hover": "#0078d4",
        "button_pressed": "#106ebe",
        "button_text": "#323130",
        "button_text_hover": "#ffffff",
        "text_color": "#323130",
        "border_radius": 5
    }

class TranslationWorker(QThread):
    """翻譯工作線程"""
    translation_complete = pyqtSignal(str, str)  # original, translation
    translation_error = pyqtSignal(str)
    progress_update = pyqtSignal(int)
    
    def __init__(self, text, source_lang='auto', target_lang='zh-tw'):
        super().__init__()
        self.text = text
        self.source_lang = source_lang
        self.target_lang = target_lang
    
    def run(self):
        try:
            print(f"[INFO] 開始翻譯: {self.text[:30]}...")
            
            self.progress_update.emit(30)
            
            from googletrans import Translator
            translator = Translator()
            
            self.progress_update.emit(60)
            
            result = translator.translate(self.text, src=self.source_lang, dest=self.target_lang)
            translation = result.text
            
            self.progress_update.emit(100)
            
            print(f"[SUCCESS] 翻譯完成: {translation[:50]}...")
            
            self.translation_complete.emit(self.text, translation)
            
        except Exception as e:
            error_msg = f"翻譯錯誤: {str(e)}"
            print(f"[ERROR] {error_msg}")
            self.translation_error.emit(error_msg)

class QTranslateStyleWindow(QWidget):
    """QTranslate風格的翻譯視窗"""
    
    def __init__(self, theme=None):
        super().__init__()
        self.theme = theme or QTranslateThemes.MODERN_BLUE_THEME
        self.translation_worker = None
        self.current_translation = ""
        self.hide_timer = QTimer()
        self.hide_timer.timeout.connect(self.hide_window)
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        # 設置視窗屬性
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setWindowTitle("QTranslate風格翻譯器")
        self.setFixedSize(480, 320)
        
        # 主佈局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        # 標題
        title_label = QLabel("🔤 QTranslate風格翻譯器")
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {self.theme['window_border']};
                font-weight: bold;
                font-size: 14px;
                padding: 5px;
            }}
        """)
        main_layout.addWidget(title_label)
        
        # 語言選擇欄
        lang_bar = self.create_language_bar()
        main_layout.addWidget(lang_bar)
        
        # 原文輸入
        source_label = QLabel("原文:")
        source_label.setStyleSheet(f"color: {self.theme['text_color']}; font-weight: bold;")
        main_layout.addWidget(source_label)
        
        self.source_text = QTextEdit()
        self.source_text.setMaximumHeight(60)
        self.source_text.setPlaceholderText("請輸入要翻譯的文字...")
        main_layout.addWidget(self.source_text)
        
        # 翻譯結果
        result_label = QLabel("翻譯結果:")
        result_label.setStyleSheet(f"color: {self.theme['text_color']}; font-weight: bold;")
        main_layout.addWidget(result_label)
        
        self.result_text = QTextEdit()
        self.result_text.setMaximumHeight(80)
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText("翻譯結果將顯示在這裡...")
        main_layout.addWidget(self.result_text)
        
        # 進度條
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # 按鈕欄
        button_bar = self.create_button_bar()
        main_layout.addWidget(button_bar)
        
        self.setLayout(main_layout)
        
        # 應用樣式
        self.apply_theme()
        
    def create_language_bar(self):
        """創建語言選擇欄"""
        lang_widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 源語言
        self.source_lang_combo = QComboBox()
        self.source_lang_combo.addItems(['自動檢測', '英語', '中文', '日語', '韓語'])
        self.source_lang_combo.setCurrentText('自動檢測')
        
        # 箭頭
        arrow_label = QLabel("→")
        arrow_label.setStyleSheet(f"color: {self.theme['text_color']}; font-size: 16px; font-weight: bold;")
        
        # 目標語言
        self.target_lang_combo = QComboBox()
        self.target_lang_combo.addItems(['繁體中文', '簡體中文', '英語', '日語', '韓語'])
        self.target_lang_combo.setCurrentText('繁體中文')
        
        layout.addWidget(QLabel("從:"))
        layout.addWidget(self.source_lang_combo)
        layout.addWidget(arrow_label)
        layout.addWidget(QLabel("到:"))
        layout.addWidget(self.target_lang_combo)
        layout.addStretch()
        
        lang_widget.setLayout(layout)
        return lang_widget
    
    def create_button_bar(self):
        """創建按鈕欄"""
        button_widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 翻譯按鈕
        translate_btn = QPushButton("🔄 翻譯")
        translate_btn.clicked.connect(self.start_translation)
        
        # 複製按鈕
        copy_btn = QPushButton("📋 複製")
        copy_btn.clicked.connect(self.copy_translation)
        
        # 清除按鈕
        clear_btn = QPushButton("🗑️ 清除")
        clear_btn.clicked.connect(self.clear_text)
        
        # 關閉按鈕
        close_btn = QPushButton("❌ 關閉")
        close_btn.clicked.connect(self.hide_window)
        
        layout.addWidget(translate_btn)
        layout.addWidget(copy_btn)
        layout.addWidget(clear_btn)
        layout.addStretch()
        layout.addWidget(close_btn)
        
        button_widget.setLayout(layout)
        return button_widget
    
    def apply_theme(self):
        """應用主題"""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.theme['window_bg']};
                color: {self.theme['text_color']};
                font-family: 'Microsoft YaHei UI', 'Segoe UI', Arial;
            }}
            QTextEdit {{
                background-color: white;
                border: 2px solid {self.theme['window_border']};
                border-radius: {self.theme['border_radius']}px;
                padding: 8px;
                font-size: 11px;
            }}
            QTextEdit:focus {{
                border-color: {self.theme['button_hover']};
            }}
            QPushButton {{
                background-color: {self.theme['button_normal']};
                border: 1px solid {self.theme['window_border']};
                border-radius: {self.theme['border_radius']}px;
                color: {self.theme['button_text']};
                padding: 8px 16px;
                font-weight: bold;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {self.theme['button_hover']};
                color: {self.theme['button_text_hover']};
            }}
            QPushButton:pressed {{
                background-color: {self.theme['button_pressed']};
            }}
            QComboBox {{
                background-color: white;
                border: 1px solid {self.theme['window_border']};
                border-radius: {self.theme['border_radius']}px;
                padding: 5px;
                min-width: 100px;
            }}
            QProgressBar {{
                border: 1px solid {self.theme['window_border']};
                border-radius: {self.theme['border_radius']}px;
                text-align: center;
                background-color: white;
            }}
            QProgressBar::chunk {{
                background-color: {self.theme['button_hover']};
                border-radius: {self.theme['border_radius']}px;
            }}
        """)
    
    def show_translation_window(self, original_text, translation):
        """顯示翻譯結果"""
        try:
            print(f"[DEBUG] 顯示翻譯視窗: {original_text[:30]} -> {translation[:30]}")
            
            # 設置文字
            self.source_text.setPlainText(original_text)
            self.result_text.setPlainText(translation)
            self.current_translation = translation
            
            # 自動複製到剪貼簿
            try:
                pyperclip.copy(translation)
                print(f"[SUCCESS] 已複製到剪貼簿")
            except Exception as e:
                print(f"[WARNING] 剪貼簿複製失敗: {e}")
            
            # 計算顯示位置（螢幕中央偏右）
            screen = QApplication.desktop().screenGeometry()
            x = (screen.width() - self.width()) // 2 + 200
            y = (screen.height() - self.height()) // 2
            self.move(x, y)
            
            # 顯示視窗
            self.show()
            self.raise_()
            self.activateWindow()
            
            print("[SUCCESS] QTranslate風格視窗已顯示")
            
            # 10秒後自動隱藏
            self.hide_timer.start(10000)
            
        except Exception as e:
            print(f"[ERROR] 顯示視窗錯誤: {e}")
    
    def start_translation(self):
        """開始翻譯"""
        text = self.source_text.toPlainText().strip()
        if not text:
            self.source_text.setPlaceholderText("請輸入要翻譯的文字!")
            return
        
        # 停止自動隱藏定時器
        self.hide_timer.stop()
        
        # 顯示進度條
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # 獲取語言設置
        source_lang = 'auto' if self.source_lang_combo.currentText() == '自動檢測' else 'en'
        target_lang = 'zh-tw' if self.target_lang_combo.currentText() == '繁體中文' else 'zh-cn'
        
        # 啟動翻譯
        self.translation_worker = TranslationWorker(text, source_lang, target_lang)
        self.translation_worker.translation_complete.connect(self.on_translation_complete)
        self.translation_worker.translation_error.connect(self.on_translation_error)
        self.translation_worker.progress_update.connect(self.progress_bar.setValue)
        self.translation_worker.start()
    
    def on_translation_complete(self, original, translation):
        """翻譯完成"""
        self.result_text.setPlainText(translation)
        self.current_translation = translation
        
        # 隱藏進度條
        self.progress_bar.setVisible(False)
        
        # 自動複製
        try:
            pyperclip.copy(translation)
        except Exception:
            pass
        
        print(f"[SUCCESS] 翻譯完成")
        
        # 重新啟動自動隱藏定時器
        self.hide_timer.start(10000)
    
    def on_translation_error(self, error):
        """翻譯錯誤"""
        self.result_text.setPlainText(f"翻譯錯誤: {error}")
        self.progress_bar.setVisible(False)
        print(f"[ERROR] 翻譯錯誤: {error}")
    
    def copy_translation(self):
        """複製翻譯結果"""
        if self.current_translation:
            pyperclip.copy(self.current_translation)
            print(f"[SUCCESS] 手動複製完成")
    
    def clear_text(self):
        """清除文字"""
        self.source_text.clear()
        self.result_text.clear()
        self.current_translation = ""
        self.hide_timer.stop()
    
    def hide_window(self):
        """隱藏視窗"""
        try:
            self.hide_timer.stop()
            self.hide()
            print("[INFO] 翻譯視窗已隱藏")
        except Exception as e:
            print(f"[WARNING] 隱藏視窗錯誤: {e}")

class QTranslateStyleTranslator(QObject):
    """QTranslate風格翻譯器主程式"""
    
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        # 創建翻譯視窗
        self.translation_window = QTranslateStyleWindow()
        
        # 設置系統托盤
        self.setup_tray()
        
        # 剪貼簿監控
        self.last_clipboard_text = ""
        
        print("[INFO] QTranslate風格翻譯器初始化完成")
    
    def setup_tray(self):
        """設置系統托盤"""
        try:
            # 創建托盤圖示
            icon_path = resource_path("icon.png")
            if not os.path.exists(icon_path):
                icon = self.app.style().standardIcon(self.app.style().SP_ComputerIcon)
            else:
                icon = QIcon(icon_path)
            
            self.tray_icon = QSystemTrayIcon(icon, self.app)
            
            # 創建托盤菜單
            tray_menu = QMenu()
            
            # 狀態顯示
            status_action = QAction("🔤 QTranslate風格翻譯器")
            status_action.setEnabled(False)
            tray_menu.addAction(status_action)
            
            tray_menu.addSeparator()
            
            # 顯示翻譯視窗
            show_action = QAction("🪟 顯示翻譯視窗")
            show_action.triggered.connect(self.show_translation_window)
            tray_menu.addAction(show_action)
            
            # 手動翻譯
            manual_action = QAction("🔤 手動翻譯 (Ctrl+C)")
            manual_action.triggered.connect(self.manual_translate)
            tray_menu.addAction(manual_action)
            
            tray_menu.addSeparator()
            
            # 退出
            quit_action = QAction("❌ 退出")
            quit_action.triggered.connect(self.quit_app)
            tray_menu.addAction(quit_action)
            
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.show()
            
            # 托盤圖示點擊事件
            self.tray_icon.activated.connect(self.tray_icon_activated)
            
            print("[SUCCESS] 系統托盤設置完成")
            
        except Exception as e:
            print(f"[ERROR] 托盤設置失敗: {e}")
    
    def setup_hotkeys(self):
        """設置熱鍵"""
        try:
            print("[INFO] 註冊熱鍵...")
            
            # 註冊Ctrl+C熱鍵
            keyboard.add_hotkey('ctrl+c', self.on_hotkey_pressed, suppress=False)
            
            print("[SUCCESS] 熱鍵註冊成功")
            
        except Exception as e:
            print(f"[WARNING] 熱鍵註冊失敗: {e}")
    
    def on_hotkey_pressed(self):
        """熱鍵按下事件"""
        try:
            # 使用QApplication定時器來避免線程問題
            QTimer.singleShot(200, self.check_and_translate_clipboard)
        except Exception as e:
            print(f"[ERROR] 熱鍵處理錯誤: {e}")
    
    def check_and_translate_clipboard(self):
        """檢查並翻譯剪貼簿內容"""
        try:
            # 獲取剪貼簿內容
            text = pyperclip.paste().strip()
            
            if not text:
                print("[INFO] 剪貼簿為空")
                return
            
            if text == self.last_clipboard_text:
                print("[INFO] 剪貼簿內容未變化")
                return
            
            # 過濾不需要翻譯的內容
            if self.should_skip_translation(text):
                print(f"[INFO] 跳過翻譯: {text[:30]}...")
                return
            
            self.last_clipboard_text = text
            
            print(f"[INFO] 檢測到新文字，準備翻譯: {text[:50]}...")
            
            # 執行翻譯
            self.translate_text(text)
            
        except Exception as e:
            print(f"[ERROR] 剪貼簿檢查錯誤: {e}")
    
    def translate_text(self, text):
        """翻譯文字並顯示結果"""
        try:
            from googletrans import Translator
            translator = Translator()
            
            print(f"[INFO] 開始翻譯: {text[:30]}...")
            
            result = translator.translate(text, src='auto', dest='zh-tw')
            translation = result.text
            
            print(f"[SUCCESS] 翻譯完成: {translation[:30]}...")
            
            # 顯示翻譯視窗
            self.translation_window.show_translation_window(text, translation)
            
        except Exception as e:
            print(f"[ERROR] 翻譯失敗: {e}")
    
    def should_skip_translation(self, text):
        """判斷是否應該跳過翻譯"""
        # 跳過純數字
        if text.isdigit():
            return True
        
        # 跳過太短的文本
        if len(text.strip()) < 2:
            return True
        
        # 跳過URL
        if text.startswith(('http://', 'https://', 'ftp://', 'www.')):
            return True
        
        # 跳過文件路徑
        if '\\' in text or text.startswith('/'):
            return True
        
        return False
    
    def show_translation_window(self):
        """顯示翻譯視窗"""
        self.translation_window.show()
        self.translation_window.raise_()
        self.translation_window.activateWindow()
    
    def manual_translate(self):
        """手動翻譯"""
        self.check_and_translate_clipboard()
    
    def tray_icon_activated(self, reason):
        """托盤圖示激活事件"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_translation_window()
    
    def quit_app(self):
        """退出應用"""
        print("[INFO] 翻譯器正在退出...")
        
        # 取消熱鍵註冊
        try:
            keyboard.unhook_all()
        except Exception as e:
            print(f"[WARNING] 熱鍵取消失敗: {e}")
        
        # 隱藏翻譯視窗
        if hasattr(self, 'translation_window'):
            self.translation_window.hide()
        
        # 退出應用
        self.app.quit()
    
    def run(self):
        """運行翻譯器"""
        try:
            print("[INFO] 啟動QTranslate風格翻譯器...")
            
            # 設置熱鍵
            self.setup_hotkeys()
            
            print("[SUCCESS] QTranslate風格翻譯器已啟動")
            print("[INFO] 按Ctrl+C進行翻譯，或右鍵點擊系統托盤圖示")
            print("[INFO] 雙擊托盤圖示顯示翻譯視窗")
            
            # 運行應用
            return self.app.exec_()
            
        except Exception as e:
            print(f"[ERROR] 翻譯器運行錯誤: {e}")
            return 1

def main():
    """主函數"""
    try:
        # 創建並運行翻譯器
        translator = QTranslateStyleTranslator()
        return translator.run()
        
    except KeyboardInterrupt:
        print("\n[INFO] 收到中斷信號，正在退出...")
        return 0
    except Exception as e:
        print(f"[ERROR] 程式運行錯誤: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 