#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM翻譯器 - QTranslate風格GUI版本
基於QTranslate 6.7.1的設計理念和界面風格

特點：
- 仿照QTranslate的界面設計和主題系統
- 支持多種主題 (Metro, Holo Light, Modern Blue)
- 無邊框視窗和自定義標題欄
- 滑動動畫效果
- 系統托盤整合
- Ctrl+C熱鍵支持
- 自動複製翻譯結果到剪貼簿
"""

import sys
import os
import json
import time
import pyperclip
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, 
                           QVBoxLayout, QHBoxLayout, QSystemTrayIcon, QMenu, QAction,
                           QTextEdit, QComboBox, QSplitter, QFrame, QScrollArea,
                           QProgressBar, QTabWidget, QListWidget, QListWidgetItem)
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer, Qt, QPoint, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor, QPixmap, QPainter, QLinearGradient
import keyboard
import psutil

def resource_path(relative_path):
    """獲取資源文件路徑"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class QTranslateThemes:
    """QTranslate主題系統"""
    
    METRO_THEME = {
        "name": "Metro",
        "window_bg": "#ffffff",
        "window_border": "#0033ff",
        "button_normal": "#d4d4d4",
        "button_hover": "#66b3ff", 
        "button_pressed": "#0033ff",
        "button_text": "#520052",
        "button_text_hover": "#ffffff",
        "text_color": "#520052",
        "border_radius": 0
    }
    
    HOLO_LIGHT_THEME = {
        "name": "Holo Light",
        "window_bg": "#f2f2f2",
        "window_border": "#bababa",
        "button_normal": "#cecece",
        "button_hover": "#ababab",
        "button_pressed": "#ababab", 
        "button_text": "#030303",
        "button_text_hover": "#030303",
        "text_color": "#000099cc",
        "border_radius": 3
    }
    
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
    translation_complete = pyqtSignal(str, str, str)  # original, translation, source_lang
    translation_error = pyqtSignal(str)
    progress_update = pyqtSignal(int)
    
    def __init__(self, text, source_lang='auto', target_lang='zh-tw'):
        super().__init__()
        self.text = text
        self.source_lang = source_lang
        self.target_lang = target_lang
    
    def run(self):
        try:
            print(f"[INFO] QTranslate風格翻譯: {self.text[:30]}...")
            
            self.progress_update.emit(30)
            
            # 使用googletrans進行翻譯
            from googletrans import Translator
            translator = Translator()
            
            self.progress_update.emit(60)
            
            result = translator.translate(self.text, src=self.source_lang, dest=self.target_lang)
            translation = result.text
            detected_lang = result.src
            
            self.progress_update.emit(100)
            
            print(f"[SUCCESS] 翻譯完成: {translation[:50]}...")
            
            self.translation_complete.emit(self.text, translation, detected_lang)
            
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
        self.animation = None
        self.init_ui()
        
    def init_ui(self):
        """初始化UI - QTranslate風格"""
        # 設置視窗屬性
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setFixedSize(500, 350)
        
        # 主佈局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(0)
        
        # 標題欄
        title_bar = self.create_title_bar()
        main_layout.addWidget(title_bar)
        
        # 內容區域
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(8)
        
        # 語言選擇欄
        lang_bar = self.create_language_bar()
        content_layout.addWidget(lang_bar)
        
        # 分隔線
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(f"color: {self.theme['window_border']};")
        content_layout.addWidget(separator)
        
        # 文本區域
        text_area = self.create_text_area()
        content_layout.addWidget(text_area)
        
        # 進度條
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {self.theme['window_border']};
                border-radius: {self.theme['border_radius']}px;
                text-align: center;
                background-color: {self.theme['window_bg']};
            }}
            QProgressBar::chunk {{
                background-color: {self.theme['button_hover']};
                border-radius: {self.theme['border_radius']}px;
            }}
        """)
        content_layout.addWidget(self.progress_bar)
        
        # 按鈕欄
        button_bar = self.create_button_bar()
        content_layout.addWidget(button_bar)
        
        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget)
        
        self.setLayout(main_layout)
        
        # 應用主題
        self.apply_theme()
        
    def create_title_bar(self):
        """創建標題欄"""
        title_widget = QWidget()
        title_widget.setFixedHeight(30)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 5, 5)
        
        # 圖示和標題
        title_label = QLabel("🔤 QTranslate風格翻譯器")
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {self.theme['text_color']};
                font-weight: bold;
                font-size: 12px;
            }}
        """)
        
        layout.addWidget(title_label)
        layout.addStretch()
        
        # 關閉按鈕
        close_btn = QPushButton("❌")
        close_btn.setFixedSize(25, 25)
        close_btn.clicked.connect(self.hide_window)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: {self.theme['text_color']};
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {self.theme['button_hover']};
                color: {self.theme['button_text_hover']};
                border-radius: 3px;
            }}
        """)
        
        layout.addWidget(close_btn)
        
        title_widget.setLayout(layout)
        return title_widget
    
    def create_language_bar(self):
        """創建語言選擇欄"""
        lang_widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 源語言
        self.source_lang_combo = QComboBox()
        self.source_lang_combo.addItems(['自動檢測', '英語', '中文', '日語', '韓語', '法語', '德語', '西班牙語'])
        self.source_lang_combo.setCurrentText('自動檢測')
        
        # 交換按鈕
        swap_btn = QPushButton("⇄")
        swap_btn.setFixedSize(35, 30)
        swap_btn.clicked.connect(self.swap_languages)
        
        # 目標語言
        self.target_lang_combo = QComboBox()
        self.target_lang_combo.addItems(['繁體中文', '簡體中文', '英語', '日語', '韓語', '法語', '德語', '西班牙語'])
        self.target_lang_combo.setCurrentText('繁體中文')
        
        # 樣式設置
        combo_style = f"""
            QComboBox {{
                background-color: {self.theme['button_normal']};
                border: 1px solid {self.theme['window_border']};
                border-radius: {self.theme['border_radius']}px;
                padding: 5px;
                color: {self.theme['button_text']};
                min-width: 100px;
            }}
            QComboBox:hover {{
                background-color: {self.theme['button_hover']};
                color: {self.theme['button_text_hover']};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: none;
                border: none;
            }}
        """
        
        self.source_lang_combo.setStyleSheet(combo_style)
        self.target_lang_combo.setStyleSheet(combo_style)
        swap_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme['button_normal']};
                border: 1px solid {self.theme['window_border']};
                border-radius: {self.theme['border_radius']}px;
                color: {self.theme['button_text']};
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.theme['button_hover']};
                color: {self.theme['button_text_hover']};
            }}
            QPushButton:pressed {{
                background-color: {self.theme['button_pressed']};
            }}
        """)
        
        layout.addWidget(self.source_lang_combo)
        layout.addWidget(swap_btn)
        layout.addWidget(self.target_lang_combo)
        
        lang_widget.setLayout(layout)
        return lang_widget
    
    def create_text_area(self):
        """創建文本區域"""
        splitter = QSplitter(Qt.Vertical)
        
        # 原文區域
        source_frame = QFrame()
        source_layout = QVBoxLayout()
        source_layout.setContentsMargins(5, 5, 5, 5)
        
        source_title = QLabel("原文:")
        source_title.setStyleSheet(f"color: {self.theme['text_color']}; font-weight: bold;")
        
        self.source_text = QTextEdit()
        self.source_text.setMaximumHeight(80)
        self.source_text.setPlaceholderText("請輸入要翻譯的文字，或按Ctrl+C從剪貼簿獲取...")
        
        source_layout.addWidget(source_title)
        source_layout.addWidget(self.source_text)
        source_frame.setLayout(source_layout)
        
        # 翻譯結果區域
        result_frame = QFrame()
        result_layout = QVBoxLayout()
        result_layout.setContentsMargins(5, 5, 5, 5)
        
        result_title = QLabel("翻譯結果:")
        result_title.setStyleSheet(f"color: {self.theme['text_color']}; font-weight: bold;")
        
        self.result_text = QTextEdit()
        self.result_text.setMaximumHeight(100)
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText("翻譯結果將顯示在這裡...")
        
        result_layout.addWidget(result_title)
        result_layout.addWidget(self.result_text)
        result_frame.setLayout(result_layout)
        
        # 文本框樣式
        text_style = f"""
            QTextEdit {{
                background-color: {self.theme['window_bg']};
                border: 2px solid {self.theme['window_border']};
                border-radius: {self.theme['border_radius']}px;
                color: {self.theme['text_color']};
                font-size: 11px;
                padding: 5px;
            }}
            QTextEdit:focus {{
                border-color: {self.theme['button_hover']};
            }}
        """
        
        self.source_text.setStyleSheet(text_style)
        self.result_text.setStyleSheet(text_style)
        
        splitter.addWidget(source_frame)
        splitter.addWidget(result_frame)
        splitter.setSizes([100, 120])
        
        return splitter
    
    def create_button_bar(self):
        """創建按鈕欄"""
        button_widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 5, 0, 0)
        
        # 翻譯按鈕
        translate_btn = QPushButton("🔄 翻譯")
        translate_btn.clicked.connect(self.start_translation)
        
        # 複製按鈕
        copy_btn = QPushButton("📋 複製")
        copy_btn.clicked.connect(self.copy_translation)
        
        # 清除按鈕
        clear_btn = QPushButton("🗑️ 清除")
        clear_btn.clicked.connect(self.clear_text)
        
        # 從剪貼簿獲取按鈕
        paste_btn = QPushButton("📥 獲取剪貼簿")
        paste_btn.clicked.connect(self.paste_from_clipboard)
        
        # 按鈕樣式
        button_style = f"""
            QPushButton {{
                background-color: {self.theme['button_normal']};
                border: 1px solid {self.theme['window_border']};
                border-radius: {self.theme['border_radius']}px;
                color: {self.theme['button_text']};
                padding: 8px 12px;
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
        """
        
        for btn in [translate_btn, copy_btn, clear_btn, paste_btn]:
            btn.setStyleSheet(button_style)
        
        layout.addWidget(translate_btn)
        layout.addWidget(copy_btn)
        layout.addWidget(clear_btn)
        layout.addWidget(paste_btn)
        layout.addStretch()
        
        button_widget.setLayout(layout)
        return button_widget
    
    def apply_theme(self):
        """應用主題"""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.theme['window_bg']};
                color: {self.theme['text_color']};
            }}
            QTranslateStyleWindow {{
                border: 2px solid {self.theme['window_border']};
                border-radius: {self.theme['border_radius']}px;
            }}
        """)
    
    def show_translation_window(self, original_text, translation):
        """顯示翻譯結果"""
        try:
            print(f"[DEBUG] QTranslate風格顯示: {original_text[:30]} -> {translation[:30]}")
            
            # 設置文字
            self.source_text.setPlainText(original_text)
            self.result_text.setPlainText(translation)
            self.current_translation = translation
            
            # 自動複製到剪貼簿
            try:
                pyperclip.copy(translation)
                print(f"[SUCCESS] 已複製到剪貼簿: {translation[:30]}...")
            except Exception as e:
                print(f"[WARNING] 剪貼簿複製失敗: {e}")
            
            # 計算顯示位置（螢幕右下角）
            screen = QApplication.desktop().screenGeometry()
            x = screen.width() - self.width() - 50
            y = screen.height() - self.height() - 100
            self.move(x, y)
            
            # 顯示視窗動畫
            self.show()
            self.raise_()
            
            # 入場動畫
            self.animate_show()
            
            print("[SUCCESS] QTranslate風格視窗已顯示")
            
            # 15秒後自動隱藏
            QTimer.singleShot(15000, self.hide_window)
            
        except Exception as e:
            print(f"[ERROR] 顯示QTranslate風格視窗錯誤: {e}")
    
    def animate_show(self):
        """入場動畫"""
        try:
            self.animation = QPropertyAnimation(self, b"geometry")
            self.animation.setDuration(300)
            self.animation.setEasingCurve(QEasingCurve.OutCubic)
            
            # 從右側滑入
            screen = QApplication.desktop().screenGeometry()
            start_x = screen.width()
            end_x = screen.width() - self.width() - 50
            y = screen.height() - self.height() - 100
            
            start_rect = QRect(start_x, y, self.width(), self.height())
            end_rect = QRect(end_x, y, self.width(), self.height())
            
            self.animation.setStartValue(start_rect)
            self.animation.setEndValue(end_rect)
            self.animation.start()
            
        except Exception as e:
            print(f"[WARNING] 動畫失敗: {e}")
    
    def start_translation(self):
        """開始翻譯"""
        text = self.source_text.toPlainText().strip()
        if not text:
            self.source_text.setPlaceholderText("請輸入要翻譯的文字!")
            return
        
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
    
    def on_translation_complete(self, original, translation, detected_lang):
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
        
        print(f"[SUCCESS] QTranslate風格翻譯完成: {translation[:30]}")
    
    def on_translation_error(self, error):
        """翻譯錯誤"""
        self.result_text.setPlainText(f"翻譯錯誤: {error}")
        self.progress_bar.setVisible(False)
        print(f"[ERROR] QTranslate風格翻譯錯誤: {error}")
    
    def copy_translation(self):
        """複製翻譯結果"""
        if self.current_translation:
            pyperclip.copy(self.current_translation)
            print(f"[SUCCESS] 手動複製: {self.current_translation[:30]}...")
    
    def clear_text(self):
        """清除文字"""
        self.source_text.clear()
        self.result_text.clear()
        self.current_translation = ""
    
    def paste_from_clipboard(self):
        """從剪貼簿獲取文字"""
        try:
            text = pyperclip.paste().strip()
            if text:
                self.source_text.setPlainText(text)
        except Exception as e:
            print(f"[ERROR] 剪貼簿獲取失敗: {e}")
    
    def swap_languages(self):
        """交換源語言和目標語言"""
        source = self.source_lang_combo.currentText()
        target = self.target_lang_combo.currentText()
        
        if source != '自動檢測':
            # 簡化的語言交換邏輯
            if '中文' in target and 'English' not in source:
                self.source_lang_combo.setCurrentText('中文')
                self.target_lang_combo.setCurrentText('英語')
            elif 'English' in source:
                self.target_lang_combo.setCurrentText('繁體中文')
    
    def hide_window(self):
        """隱藏視窗"""
        try:
            self.hide()
            print("[INFO] QTranslate風格視窗已隱藏")
        except Exception as e:
            print(f"[WARNING] 隱藏視窗錯誤: {e}")

class QTranslateStyleTranslator(QObject):
    """QTranslate風格翻譯器主程式"""
    
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        # 載入配置
        self.load_config()
        
        # 創建QTranslate風格翻譯視窗
        self.translation_window = QTranslateStyleWindow(QTranslateThemes.MODERN_BLUE_THEME)
        
        # 設置系統托盤
        self.setup_tray()
        
        # 剪貼簿監控
        self.last_clipboard_text = ""
        
        print("[INFO] QTranslate風格翻譯器初始化完成")
    
    def load_config(self):
        """載入配置"""
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"[WARNING] 配置載入失敗: {e}")
            self.config = {
                "hotkeys": {"manual_translate": "ctrl+c"},
                "translation": {"default_target": "zh-TW"},
                "auto_translate": True
            }
    
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
            self.status_action = QAction("🔤 QTranslate風格翻譯器", self.app)
            self.status_action.setEnabled(False)
            tray_menu.addAction(self.status_action)
            
            tray_menu.addSeparator()
            
            # 顯示翻譯視窗
            show_action = QAction("🪟 顯示翻譯視窗", self.app)
            show_action.triggered.connect(self.show_translation_window)
            tray_menu.addAction(show_action)
            
            # 手動翻譯
            manual_action = QAction("🔤 手動翻譯 (Ctrl+C)", self.app)
            manual_action.triggered.connect(self.manual_translate)
            tray_menu.addAction(manual_action)
            
            # 主題選擇
            theme_menu = QMenu("🎨 主題選擇", self.app)
            
            metro_action = QAction("Metro", self.app)
            metro_action.triggered.connect(lambda: self.change_theme(QTranslateThemes.METRO_THEME))
            theme_menu.addAction(metro_action)
            
            holo_action = QAction("Holo Light", self.app)
            holo_action.triggered.connect(lambda: self.change_theme(QTranslateThemes.HOLO_LIGHT_THEME))
            theme_menu.addAction(holo_action)
            
            modern_action = QAction("Modern Blue", self.app)
            modern_action.triggered.connect(lambda: self.change_theme(QTranslateThemes.MODERN_BLUE_THEME))
            theme_menu.addAction(modern_action)
            
            tray_menu.addMenu(theme_menu)
            
            tray_menu.addSeparator()
            
            # 退出
            quit_action = QAction("❌ 退出", self.app)
            quit_action.triggered.connect(self.quit_app)
            tray_menu.addAction(quit_action)
            
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.show()
            
            # 托盤圖示點擊事件
            self.tray_icon.activated.connect(self.tray_icon_activated)
            
            print("[SUCCESS] QTranslate風格系統托盤設置完成")
            
        except Exception as e:
            print(f"[ERROR] 托盤設置失敗: {e}")
    
    def setup_hotkeys(self):
        """設置熱鍵"""
        try:
            print("[INFO] 註冊QTranslate風格熱鍵...")
            
            # 註冊Ctrl+C熱鍵
            keyboard.add_hotkey('ctrl+c', self.on_hotkey_pressed, suppress=False)
            
            print("[SUCCESS] QTranslate風格熱鍵註冊成功")
            
        except Exception as e:
            print(f"[WARNING] 熱鍵註冊失敗: {e}")
    
    def on_hotkey_pressed(self):
        """熱鍵按下事件"""
        try:
            # 等待一小段時間讓剪貼簿更新
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
            
            # 直接顯示翻譯視窗並開始翻譯
            self.translation_window.source_text.setPlainText(text)
            self.translation_window.show()
            self.translation_window.raise_()
            self.translation_window.start_translation()
            
        except Exception as e:
            print(f"[ERROR] 剪貼簿檢查錯誤: {e}")
    
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
    
    def manual_translate(self):
        """手動翻譯"""
        self.check_and_translate_clipboard()
    
    def change_theme(self, theme):
        """更換主題"""
        self.translation_window.theme = theme
        self.translation_window.apply_theme()
        print(f"[INFO] 主題已更換為: {theme['name']}")
    
    def tray_icon_activated(self, reason):
        """托盤圖示激活事件"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_translation_window()
    
    def quit_app(self):
        """退出應用"""
        print("[INFO] QTranslate風格翻譯器正在退出...")
        
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
            print(f"[ERROR] QTranslate風格翻譯器運行錯誤: {e}")
            return 1

def main():
    """主函數"""
    try:
        # 檢查是否已經有實例在運行
        current_pid = os.getpid()
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['pid'] != current_pid and 'python' in proc.info['name'].lower():
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    if 'translator_qtranslate_style.py' in cmdline:
                        print(f"[WARNING] 檢測到另一個翻譯器實例正在運行 (PID: {proc.info['pid']})")
                        choice = input("是否要終止舊實例並啟動新的? (y/N): ").strip().lower()
                        if choice == 'y':
                            proc.terminate()
                            proc.wait(timeout=5)
                            print("[INFO] 舊實例已終止")
                        else:
                            print("[INFO] 保持舊實例運行，退出")
                            return 0
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
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