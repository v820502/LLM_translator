#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
調試翻譯彈窗功能
"""

import sys
import pyperclip
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

class SimpleTranslatorWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 防止窗口關閉時退出應用程序
        self.setAttribute(Qt.WA_QuitOnClose, False)
        self.initUI()
        
    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        layout = QVBoxLayout()
        
        # 翻譯結果顯示區域
        self.result_label = QLabel("測試翻譯窗口")
        self.result_label.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                min-height: 60px;
            }
        """)
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)
        
        # 按鈕區域
        button_layout = QHBoxLayout()
        
        # 關閉按鈕
        close_button = QPushButton("關閉")
        close_button.clicked.connect(self.hide)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
    def show_at_mouse(self):
        """在滑鼠位置顯示窗口"""
        try:
            print("🖱️ Getting mouse position...")
            cursor_pos = QCursor.pos()
            print(f"🖱️ Mouse position: {cursor_pos.x()}, {cursor_pos.y()}")
            
            print("📐 Getting screen geometry...")
            screen = QApplication.desktop().screenGeometry()
            print(f"📐 Screen size: {screen.width()}x{screen.height()}")
            
            # 確保位置在螢幕範圍內
            x = max(0, min(cursor_pos.x(), screen.width() - 300))  # 假設窗口寬度300
            y = max(0, min(cursor_pos.y(), screen.height() - 200))  # 假設窗口高度200
            
            print(f"📍 Moving to position: {x}, {y}")
            self.move(x, y)
            
            print("👁️ Showing window...")
            self.show()
            self.raise_()
            self.activateWindow()
            
            print("✅ Window shown successfully")
            
        except Exception as e:
            print(f"❌ Error showing window: {e}")
            import traceback
            traceback.print_exc()

def test_popup():
    """測試彈窗功能"""
    print("🔧 測試翻譯彈窗功能...")
    
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # 創建測試窗口
    window = SimpleTranslatorWindow()
    
    print("📋 複製測試文本到剪貼板...")
    pyperclip.copy("Hello World")
    
    print("🖱️ 在滑鼠位置顯示彈窗...")
    window.show_at_mouse()
    
    print("⏳ 窗口已顯示，5秒後自動關閉...")
    
    # 5秒後自動關閉窗口
    from PyQt5.QtCore import QTimer
    QTimer.singleShot(5000, window.hide)
    QTimer.singleShot(5500, app.quit)
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_popup() 