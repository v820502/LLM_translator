#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM翻譯器 - 修復後的GUI版本
修復視窗卡住問題，但保留彈出視窗功能
"""

import sys
import os
import json
import time
import threading
import sqlite3
import requests
import pyperclip
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, 
                           QVBoxLayout, QHBoxLayout, QSystemTrayIcon, QMenu, QAction,
                           QSizePolicy, QSpacerItem)
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer, Qt, QPoint
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
import keyboard
import psutil

def resource_path(relative_path):
    """獲取資源文件路徑"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SimpleTranslationWorker(QThread):
    """簡化的翻譯工作線程"""
    translation_complete = pyqtSignal(str, str)  # original, translation
    translation_error = pyqtSignal(str)
    
    def __init__(self, text, target_lang='zh-tw'):
        super().__init__()
        self.text = text
        self.target_lang = target_lang
    
    def run(self):
        try:
            print(f"[INFO] 開始翻譯: {self.text[:30]}...")
            
            # 使用googletrans進行翻譯
            from googletrans import Translator
            translator = Translator()
            
            result = translator.translate(self.text, dest=self.target_lang)
            translation = result.text
            
            print(f"[SUCCESS] 翻譯完成: {translation[:50]}...")
            
            self.translation_complete.emit(self.text, translation)
            
        except Exception as e:
            error_msg = f"翻譯錯誤: {str(e)}"
            print(f"[ERROR] {error_msg}")
            self.translation_error.emit(error_msg)

class FixedTranslationWindow(QWidget):
    """修復後的翻譯結果視窗"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.hide_timer = None
        
    def init_ui(self):
        """初始化UI"""
        # 設置視窗屬性 - 簡化版本
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, False)  # 不使用透明背景
        self.setFixedSize(400, 150)
        
        # 創建佈局
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # 結果標籤
        self.result_label = QLabel()
        self.result_label.setWordWrap(True)
        self.result_label.setAlignment(Qt.AlignCenter)
        
        # 設置字體
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.result_label.setFont(font)
        
        # 複製按鈕
        self.copy_button = QPushButton("📋 複製翻譯")
        self.copy_button.setFixedHeight(35)
        self.copy_button.clicked.connect(self.copy_translation)
        
        # 關閉按鈕
        self.close_button = QPushButton("❌ 關閉")
        self.close_button.setFixedHeight(35)
        self.close_button.clicked.connect(self.hide_window)
        
        # 按鈕佈局
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.close_button)
        
        # 添加到主佈局
        layout.addWidget(self.result_label)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # 設置樣式
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border: 2px solid #333;
                border-radius: 10px;
            }
            QLabel {
                background-color: transparent;
                color: #000;
                padding: 10px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        
        # 存儲翻譯結果
        self.current_translation = ""
        
    def show_translation(self, original_text, translation):
        """顯示翻譯結果"""
        try:
            print(f"[DEBUG] 顯示翻譯: {original_text[:30]} -> {translation[:30]}")
            
            # 設置文字
            display_text = f"原文: {original_text}\n\n翻譯: {translation}"
            self.result_label.setText(display_text)
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
            
            # 顯示視窗
            self.show()
            self.raise_()
            self.activateWindow()
            
            print("[SUCCESS] 翻譯視窗已顯示")
            
            # 設定自動隱藏（10秒後）
            self.start_auto_hide_timer()
            
        except Exception as e:
            print(f"[ERROR] 顯示翻譯視窗錯誤: {e}")
            import traceback
            traceback.print_exc()
    
    def start_auto_hide_timer(self):
        """啟動自動隱藏定時器"""
        try:
            # 清除舊定時器
            if self.hide_timer:
                self.hide_timer.stop()
                self.hide_timer = None
            
            # 創建新定時器
            self.hide_timer = QTimer()
            self.hide_timer.setSingleShot(True)
            self.hide_timer.timeout.connect(self.hide_window)
            self.hide_timer.start(10000)  # 10秒後自動隱藏
            
        except Exception as e:
            print(f"[WARNING] 定時器設置失敗: {e}")
    
    def copy_translation(self):
        """複製翻譯結果"""
        try:
            if self.current_translation:
                pyperclip.copy(self.current_translation)
                self.copy_button.setText("✅ 已複製")
                # 2秒後恢復按鈕文字
                QTimer.singleShot(2000, lambda: self.copy_button.setText("📋 複製翻譯"))
                print(f"[SUCCESS] 手動複製: {self.current_translation[:30]}...")
        except Exception as e:
            print(f"[ERROR] 複製失敗: {e}")
    
    def hide_window(self):
        """隱藏視窗"""
        try:
            if self.hide_timer:
                self.hide_timer.stop()
                self.hide_timer = None
            self.hide()
            print("[INFO] 翻譯視窗已隱藏")
        except Exception as e:
            print(f"[WARNING] 隱藏視窗錯誤: {e}")
    
    def enterEvent(self, event):
        """滑鼠進入時停止自動隱藏"""
        if self.hide_timer:
            self.hide_timer.stop()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """滑鼠離開時重新開始自動隱藏"""
        self.start_auto_hide_timer()
        super().leaveEvent(event)

class FixedGUITranslator(QObject):
    """修復後的GUI翻譯器"""
    
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        # 載入配置
        self.load_config()
        
        # 創建翻譯視窗
        self.translation_window = FixedTranslationWindow()
        
        # 設置系統托盤
        self.setup_tray()
        
        # 翻譯工作線程
        self.translation_worker = None
        
        # 剪貼簿監控
        self.clipboard_monitor_active = True
        self.last_clipboard_text = ""
        
        print("[INFO] 修復版GUI翻譯器初始化完成")
    
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
            self.status_action = QAction("🔄 準備就緒", self.app)
            self.status_action.setEnabled(False)
            tray_menu.addAction(self.status_action)
            
            tray_menu.addSeparator()
            
            # 手動翻譯
            manual_action = QAction("🔤 手動翻譯 (Ctrl+C)", self.app)
            manual_action.triggered.connect(self.manual_translate)
            tray_menu.addAction(manual_action)
            
            # 自動翻譯開關
            self.auto_action = QAction("✅ 自動翻譯", self.app)
            self.auto_action.setCheckable(True)
            self.auto_action.setChecked(self.config.get('auto_translate', True))
            self.auto_action.triggered.connect(self.toggle_auto_translate)
            tray_menu.addAction(self.auto_action)
            
            # 顯示翻譯視窗
            show_window_action = QAction("🪟 顯示翻譯視窗", self.app)
            show_window_action.triggered.connect(self.show_translation_window)
            tray_menu.addAction(show_window_action)
            
            tray_menu.addSeparator()
            
            # 退出
            quit_action = QAction("❌ 退出", self.app)
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
            # 等待一小段時間讓剪貼簿更新
            QTimer.singleShot(100, self.check_and_translate_clipboard)
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
            self.start_translation(text)
            
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
    
    def start_translation(self, text):
        """開始翻譯"""
        try:
            print(f"[INFO] 準備翻譯: {text[:50]}...")
            
            # 更新托盤狀態
            self.status_action.setText("🔄 翻譯中...")
            
            # 停止之前的翻譯工作
            if self.translation_worker and self.translation_worker.isRunning():
                self.translation_worker.terminate()
                self.translation_worker.wait(1000)
            
            # 創建新的翻譯工作線程
            target_lang = self.config.get('translation', {}).get('default_target', 'zh-tw')
            self.translation_worker = SimpleTranslationWorker(text, target_lang)
            
            # 連接信號
            self.translation_worker.translation_complete.connect(self.on_translation_complete)
            self.translation_worker.translation_error.connect(self.on_translation_error)
            
            # 啟動翻譯
            self.translation_worker.start()
            
        except Exception as e:
            print(f"[ERROR] 翻譯啟動失敗: {e}")
            self.status_action.setText("❌ 翻譯失敗")
    
    def on_translation_complete(self, original, translation):
        """翻譯完成回調"""
        try:
            print(f"[SUCCESS] 翻譯完成: {original[:30]} -> {translation[:30]}")
            
            # 更新托盤狀態
            self.status_action.setText("✅ 翻譯完成")
            
            # 顯示翻譯視窗
            self.translation_window.show_translation(original, translation)
            
            # 顯示系統通知
            if self.tray_icon.supportsMessages():
                self.tray_icon.showMessage(
                    "翻譯完成", 
                    f"翻譯: {translation[:50]}...", 
                    QSystemTrayIcon.Information, 
                    3000
                )
            
            # 重置狀態
            QTimer.singleShot(3000, lambda: self.status_action.setText("🔄 準備就緒"))
            
        except Exception as e:
            print(f"[ERROR] 翻譯完成處理錯誤: {e}")
    
    def on_translation_error(self, error):
        """翻譯錯誤回調"""
        print(f"[ERROR] 翻譯錯誤: {error}")
        self.status_action.setText("❌ 翻譯失敗")
        
        # 顯示錯誤通知
        if self.tray_icon.supportsMessages():
            self.tray_icon.showMessage("翻譯失敗", error, QSystemTrayIcon.Critical, 3000)
        
        # 重置狀態
        QTimer.singleShot(3000, lambda: self.status_action.setText("🔄 準備就緒"))
    
    def manual_translate(self):
        """手動翻譯"""
        self.check_and_translate_clipboard()
    
    def show_translation_window(self):
        """顯示翻譯視窗"""
        if hasattr(self, 'translation_window'):
            self.translation_window.show()
            self.translation_window.raise_()
    
    def toggle_auto_translate(self):
        """切換自動翻譯"""
        auto_enabled = self.auto_action.isChecked()
        self.config['auto_translate'] = auto_enabled
        
        if auto_enabled:
            self.auto_action.setText("✅ 自動翻譯")
            print("[INFO] 自動翻譯已啟用")
        else:
            self.auto_action.setText("⭕ 自動翻譯")
            print("[INFO] 自動翻譯已禁用")
        
        # 保存配置
        try:
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[WARNING] 配置保存失敗: {e}")
    
    def tray_icon_activated(self, reason):
        """托盤圖示激活事件"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.manual_translate()
    
    def quit_app(self):
        """退出應用"""
        print("[INFO] 正在退出...")
        
        # 停止翻譯工作
        if self.translation_worker and self.translation_worker.isRunning():
            self.translation_worker.terminate()
            self.translation_worker.wait(1000)
        
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
            print("[INFO] 啟動修復版GUI翻譯器...")
            
            # 設置熱鍵
            self.setup_hotkeys()
            
            # 啟動剪貼簿監控（如果啟用自動翻譯）
            if self.config.get('auto_translate', True):
                print("[INFO] 自動翻譯已啟用")
            
            print("[SUCCESS] GUI翻譯器已啟動，按Ctrl+C進行翻譯")
            print("[INFO] 翻譯結果將在彈出視窗中顯示")
            print("[INFO] 查看系統托盤圖示進行更多操作")
            
            # 運行應用
            return self.app.exec_()
            
        except Exception as e:
            print(f"[ERROR] 翻譯器運行錯誤: {e}")
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
                    if 'translator_fixed_gui.py' in cmdline:
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
        translator = FixedGUITranslator()
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