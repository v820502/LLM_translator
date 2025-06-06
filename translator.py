import sys
import os
import pyperclip
import json
import requests
import sqlite3
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from PyQt5.QtWidgets import (QApplication, QSystemTrayIcon, QMenu, 
                            QWidget, QVBoxLayout, QLabel, QPushButton, QAction,
                            QDialog, QFormLayout, QLineEdit, QComboBox, 
                            QTextEdit, QCheckBox, QTabWidget, QHBoxLayout,
                            QSpacerItem, QSizePolicy, QMessageBox, QTableWidget,
                            QTableWidgetItem, QHeaderView, QSplitter, QGroupBox,
                            QListWidget, QListWidgetItem, QProgressBar, QFrame,
                            QScrollArea, QDesktopWidget)
from PyQt5.QtCore import Qt, QPoint, QThread, pyqtSignal, QTimer, QSize, QObject
from PyQt5.QtGui import QIcon, QCursor, QFont, QPixmap
import tempfile
import subprocess
import re
import time
import threading
from urllib.parse import quote
import base64

def resource_path(relative_path):
    """獲取資源的絕對路徑"""
    try:
        # PyInstaller 創建的臨時文件夾
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# QTranslate-inspired enhancements
class QTranslateAdvancedFeatures:
    """Advanced features inspired by QTranslate 6.7.1"""
    
    # Translation service capabilities (from QTranslate)
    CAPABILITY_TRANSLATE = 1
    CAPABILITY_DETECT_LANGUAGE = 2  
    CAPABILITY_LISTEN = 4
    CAPABILITY_DICTIONARY = 8
    
    # Mouse modes (from QTranslate)
    MOUSE_MODE_DISABLED = 0
    MOUSE_MODE_ICON_SHOW = 1
    MOUSE_MODE_INSTANT_TRANSLATE = 2
    MOUSE_MODE_INSTANT_TRANSLATE_AND_LISTEN = 3
    
    # Popup timeout and positioning
    DEFAULT_POPUP_TIMEOUT = 5  # seconds
    MAX_QUERY_LENGTH = 5000
    MAX_URI_LENGTH = 2048

class ThemeManager:
    """Advanced theming system inspired by QTranslate themes"""
    
    def __init__(self):
        self.themes = {
            "Photoshop Dark": {
                "Common": {
                    "ButtonRadius": 2,
                    "WindowBorderRadius": 1,
                    "ClientBackColor": "#353535",
                    "GroupBoxColor": "#383838",
                    "GroupBoxHighlightColor": "#707070",
                    "PaintClassicFocus": False
                },
                "Window": {
                    "Normal": {
                        "Back": "#353535",
                        "Text": "#f5f5f5",
                        "Border": "#363636",
                        "BorderInner": "#656565",
                        "Caption": ""
                    }
                },
                "Button": {
                    "Normal": {
                        "Border": "#272727",
                        "BackTop": "#757575",
                        "BackBottom": "#626262",
                        "Text": "#ffffff"
                    },
                    "Pressed": {
                        "Border": "#272727",
                        "BackTop": "#3f3f3f",
                        "BackBottom": "#373737",
                        "Text": "#ffffff"
                    },
                    "Focused": {
                        "Border": "#506fac",
                        "BackTop": "#757575",
                        "BackBottom": "#626262",
                        "Text": "#ffffff"
                    }
                },
                "Edit": {
                    "Normal": {
                        "Border": "#272727",
                        "Back": "#3a3a3a",
                        "Text": "#dddddd"
                    },
                    "Focused": {
                        "Border": "#506fac",
                        "Back": "#3a3a3a",
                        "Text": "#dddddd"
                    }
                }
            },
            "Holo Light": {
                "Common": {
                    "ButtonRadius": 3,
                    "WindowBorderRadius": 2,
                    "ClientBackColor": "#f5f5f5",
                    "GroupBoxColor": "#e8e8e8",
                    "GroupBoxHighlightColor": "#0099cc",
                    "PaintClassicFocus": True
                },
                "Window": {
                    "Normal": {
                        "Back": "#f5f5f5",
                        "Text": "#333333",
                        "Border": "#cccccc",
                        "BorderInner": "#e0e0e0",
                        "Caption": ""
                    }
                },
                "Button": {
                    "Normal": {
                        "Border": "#cccccc",
                        "BackTop": "#ffffff",
                        "BackBottom": "#eeeeee",
                        "Text": "#333333"
                    },
                    "Pressed": {
                        "Border": "#0099cc",
                        "BackTop": "#0099cc",
                        "BackBottom": "#0088bb",
                        "Text": "#ffffff"
                    },
                    "Focused": {
                        "Border": "#0099cc",
                        "BackTop": "#ffffff",
                        "BackBottom": "#eeeeee",
                        "Text": "#333333"
                    }
                },
                "Edit": {
                    "Normal": {
                        "Border": "#cccccc",
                        "Back": "#ffffff",
                        "Text": "#333333"
                    },
                    "Focused": {
                        "Border": "#0099cc",
                        "Back": "#ffffff",
                        "Text": "#333333"
                    }
                }
            },
            "Metro": {
                "Common": {
                    "ButtonRadius": 0,
                    "WindowBorderRadius": 0,
                    "ClientBackColor": "#2d2d30",
                    "GroupBoxColor": "#3f3f46",
                    "GroupBoxHighlightColor": "#007acc",
                    "PaintClassicFocus": False
                },
                "Window": {
                    "Normal": {
                        "Back": "#2d2d30",
                        "Text": "#ffffff",
                        "Border": "#3f3f46",
                        "BorderInner": "#007acc",
                        "Caption": ""
                    }
                },
                "Button": {
                    "Normal": {
                        "Border": "#3f3f46",
                        "BackTop": "#007acc",
                        "BackBottom": "#007acc",
                        "Text": "#ffffff"
                    },
                    "Pressed": {
                        "Border": "#007acc",
                        "BackTop": "#005a9e",
                        "BackBottom": "#005a9e",
                        "Text": "#ffffff"
                    },
                    "Focused": {
                        "Border": "#007acc",
                        "BackTop": "#007acc",
                        "BackBottom": "#007acc",
                        "Text": "#ffffff"
                    }
                },
                "Edit": {
                    "Normal": {
                        "Border": "#3f3f46",
                        "Back": "#1e1e1e",
                        "Text": "#ffffff"
                    },
                    "Focused": {
                        "Border": "#007acc",
                        "Back": "#1e1e1e",
                        "Text": "#ffffff"
                    }
                }
            },
            "Blue": {
                "Common": {
                    "ButtonRadius": 2,
                    "WindowBorderRadius": 1,
                    "ClientBackColor": "#1e3a5f",
                    "GroupBoxColor": "#2e4a6f",
                    "GroupBoxHighlightColor": "#4a8bc2",
                    "PaintClassicFocus": True
                },
                "Window": {
                    "Normal": {
                        "Back": "#1e3a5f",
                        "Text": "#ffffff",
                        "Border": "#2e4a6f",
                        "BorderInner": "#4a8bc2",
                        "Caption": ""
                    }
                },
                "Button": {
                    "Normal": {
                        "Border": "#2e4a6f",
                        "BackTop": "#4a8bc2",
                        "BackBottom": "#3a7bb2",
                        "Text": "#ffffff"
                    },
                    "Pressed": {
                        "Border": "#2e4a6f",
                        "BackTop": "#2a6ba2",
                        "BackBottom": "#1a5b92",
                        "Text": "#ffffff"
                    },
                    "Focused": {
                        "Border": "#4a8bc2",
                        "BackTop": "#4a8bc2",
                        "BackBottom": "#3a7bb2",
                        "Text": "#ffffff"
                    }
                },
                "Edit": {
                    "Normal": {
                        "Border": "#2e4a6f",
                        "Back": "#0e2a4f",
                        "Text": "#ffffff"
                    },
                    "Focused": {
                        "Border": "#4a8bc2",
                        "Back": "#0e2a4f",
                        "Text": "#ffffff"
                    }
                }
            },
            "Flat Dark": {
                "Common": {
                    "ButtonRadius": 4,
                    "WindowBorderRadius": 6,
                    "ClientBackColor": "#2b2b2b",
                    "GroupBoxColor": "#3c3c3c",
                    "GroupBoxHighlightColor": "#00d4aa",
                    "PaintClassicFocus": False
                },
                "Window": {
                    "Normal": {
                        "Back": "#2b2b2b",
                        "Text": "#ffffff",
                        "Border": "#3c3c3c",
                        "BorderInner": "#00d4aa",
                        "Caption": ""
                    }
                },
                "Button": {
                    "Normal": {
                        "Border": "#3c3c3c",
                        "BackTop": "#00d4aa",
                        "BackBottom": "#00d4aa",
                        "Text": "#ffffff"
                    },
                    "Pressed": {
                        "Border": "#00d4aa",
                        "BackTop": "#00b897",
                        "BackBottom": "#00b897",
                        "Text": "#ffffff"
                    },
                    "Focused": {
                        "Border": "#00d4aa",
                        "BackTop": "#00d4aa",
                        "BackBottom": "#00d4aa",
                        "Text": "#ffffff"
                    }
                },
                "Edit": {
                    "Normal": {
                        "Border": "#3c3c3c",
                        "Back": "#1e1e1e",
                        "Text": "#ffffff"
                    },
                    "Focused": {
                        "Border": "#00d4aa",
                        "Back": "#1e1e1e",
                        "Text": "#ffffff"
                    }
                }
            }
        }
        self.current_theme = "Photoshop Dark"
    
    def get_current_theme(self):
        return self.themes.get(self.current_theme, self.themes["Photoshop Dark"])
    
    def set_theme(self, theme_name: str):
        if theme_name in self.themes:
            self.current_theme = theme_name
    
    def get_stylesheet(self, widget_type: str = "Window") -> str:
        """Generate Qt stylesheet from theme data"""
        theme = self.get_current_theme()
        
        if widget_type == "Window":
            window = theme["Window"]["Normal"]
            return f"""
                QWidget {{
                    background-color: {window["Back"]};
                    color: {window["Text"]};
                    border: 1px solid {window["Border"]};
                    border-radius: {theme["Common"]["WindowBorderRadius"]}px;
                }}
            """
        elif widget_type == "Button":
            button = theme["Button"]["Normal"]
            button_pressed = theme["Button"]["Pressed"]
            button_focused = theme["Button"]["Focused"]
            return f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 {button["BackTop"]}, stop:1 {button["BackBottom"]});
                    border: 1px solid {button["Border"]};
                    border-radius: {theme["Common"]["ButtonRadius"]}px;
                    color: {button["Text"]};
                    padding: 5px 15px;
                    font-weight: bold;
                }}
                QPushButton:pressed {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 {button_pressed["BackTop"]}, stop:1 {button_pressed["BackBottom"]});
                    border: 1px solid {button_pressed["Border"]};
                }}
                QPushButton:focus {{
                    border: 2px solid {button_focused["Border"]};
                }}
            """
        elif widget_type == "Edit":
            edit = theme["Edit"]["Normal"]
            edit_focused = theme["Edit"]["Focused"]
            return f"""
                QLineEdit, QTextEdit, QPlainTextEdit {{
                    background-color: {edit["Back"]};
                    color: {edit["Text"]};
                    border: 1px solid {edit["Border"]};
                    border-radius: 2px;
                    padding: 4px;
                }}
                QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
                    border: 2px solid {edit_focused["Border"]};
                }}
            """
        
        return ""

class AdvancedHotkeyManager:
    """Enhanced hotkey system inspired by QTranslate"""
    
    def __init__(self, translator_app):
        self.app = translator_app
        self.hotkeys = {
            'main_window': 'ctrl+ctrl',  # Double Ctrl
            'popup_window': 'ctrl+q',
            'web_search': 'ctrl+shift+q',
            'listen_text': 'ctrl+e',
            'clear_translation': 'ctrl+n',
            'dictionary': 'ctrl+d',
            'history': 'ctrl+h',
            'virtual_keyboard': 'ctrl+k',
            'switch_languages': 'ctrl+i',
            'fullscreen': 'f11',
            'help': 'f1',
            'previous_translation': 'alt+left',
            'next_translation': 'alt+right',
            'copy_to_dictionary': 'ctrl+up',
            'manual_translate': 'ctrl+shift+t',
            'replace_selection': 'ctrl+shift+r',
            'ocr_translate': 'ctrl+shift+o',
            'speech_input': 'ctrl+shift+s'
        }
        self.enabled = True
    
    def register_hotkeys(self):
        """Register all hotkeys"""
        # Note: In actual implementation, this would register the hotkeys
        # For now, we'll skip actual registration to avoid conflicts
        pass
    
    def unregister_hotkeys(self):
        """Unregister all hotkeys"""
        try:
            keyboard.unhook_all_hotkeys()
        except Exception as e:
            print(f"Hotkey unregistration error: {e}")

class OCRTranslator:
    """OCR-based translation system"""
    
    def __init__(self):
        self.ocr_api_key = ""
        self.supported_languages = ["auto", "en", "zh", "ja", "ko", "fr", "de", "es", "it", "pt", "ru", "ar"]
    
    def capture_screen_area(self):
        """Capture a screen area for OCR"""
        # Placeholder for screen capture functionality
        return None
    
    def extract_text_from_image(self, image_data: bytes, language: str = "auto") -> str:
        """Extract text from image using OCR API"""
        # Placeholder for OCR functionality
        return "OCR text extraction would be implemented here"
    
    def start_screen_capture(self, callback):
        """Start interactive screen capture for OCR"""
        # Placeholder for screen capture
        callback("Screen capture would be implemented here")

class MultiServiceTranslator:
    """Enhanced translation service manager supporting multiple providers"""
    
    def __init__(self):
        self.services = {
            "google": {
                "name": "Google Translate",
                "capabilities": QTranslateAdvancedFeatures.CAPABILITY_TRANSLATE | 
                              QTranslateAdvancedFeatures.CAPABILITY_DETECT_LANGUAGE |
                              QTranslateAdvancedFeatures.CAPABILITY_LISTEN,
                "languages": ["auto", "af", "sq", "ar", "hy", "az", "eu", "be", "bg", "ca", 
                             "zh-cn", "zh-tw", "hr", "cs", "da", "nl", "en", "et", "fi", "fr",
                             "gl", "de", "el", "gu", "ht", "he", "hi", "hu", "is", "id", "ga",
                             "it", "ja", "kn", "ko", "la", "lv", "lt", "mk", "ms", "mt", "no",
                             "fa", "pl", "pt", "ro", "ru", "sr", "sk", "sl", "es", "sw", "sv",
                             "ta", "te", "th", "tr", "uk", "ur", "vi", "cy", "yi"]
            },
            "deepl": {
                "name": "DeepL Translator",
                "capabilities": QTranslateAdvancedFeatures.CAPABILITY_TRANSLATE | 
                              QTranslateAdvancedFeatures.CAPABILITY_DETECT_LANGUAGE,
                "languages": ["auto", "bg", "cs", "da", "de", "el", "en", "es", "et", "fi", "fr", 
                             "hu", "it", "ja", "lt", "lv", "nl", "pl", "pt", "ro", "ru", "sk", 
                             "sl", "sv", "zh"]
            },
            "microsoft": {
                "name": "Microsoft Translator",
                "capabilities": QTranslateAdvancedFeatures.CAPABILITY_TRANSLATE | 
                              QTranslateAdvancedFeatures.CAPABILITY_DETECT_LANGUAGE |
                              QTranslateAdvancedFeatures.CAPABILITY_LISTEN,
                "languages": ["auto", "af", "ar", "bg", "bn", "bs", "ca", "cs", "cy", "da", "de", 
                             "el", "en", "es", "et", "fa", "fi", "fr", "ga", "gu", "he", "hi", 
                             "hr", "hu", "is", "it", "ja", "kn", "ko", "lt", "lv", "mk", "ml", 
                             "mr", "ms", "mt", "nb", "nl", "pa", "pl", "pt", "ro", "ru", "sk", 
                             "sl", "sr", "sv", "sw", "ta", "te", "th", "tr", "uk", "ur", "vi", 
                             "zh-Hans", "zh-Hant"]
            },
            "yandex": {
                "name": "Yandex Translate",
                "capabilities": QTranslateAdvancedFeatures.CAPABILITY_TRANSLATE | 
                              QTranslateAdvancedFeatures.CAPABILITY_DETECT_LANGUAGE,
                "languages": ["auto", "az", "sq", "am", "en", "ar", "hy", "af", "eu", "ba", "be", 
                             "bn", "my", "bg", "bs", "cy", "hu", "vi", "ht", "gl", "nl", "mrj", 
                             "el", "ka", "gu", "da", "he", "yi", "id", "ga", "it", "is", "es", 
                             "kk", "kn", "ca", "ky", "zh", "ko", "xh", "km", "lo", "la", "lv", 
                             "lt", "lb", "mg", "ms", "ml", "mt", "mk", "mi", "mr", "mhr", "mn", 
                             "de", "ne", "no", "pa", "pap", "fa", "pl", "pt", "ro", "ru", "ceb", 
                             "sr", "si", "sk", "sl", "sw", "su", "tg", "th", "tl", "ta", "tt", 
                             "te", "tr", "udm", "uz", "uk", "ur", "fi", "fr", "hi", "hr", "cs", 
                             "sv", "gd", "et", "eo", "jv", "ja"]
            },
            "baidu": {
                "name": "Baidu Translate",
                "capabilities": QTranslateAdvancedFeatures.CAPABILITY_TRANSLATE | 
                              QTranslateAdvancedFeatures.CAPABILITY_DETECT_LANGUAGE,
                "languages": ["auto", "zh", "en", "yue", "wyw", "jp", "kor", "spa", "fra", "th", 
                             "ara", "ru", "pt", "de", "it", "el", "nl", "pl", "bul", "est", "dan", 
                             "fin", "cs", "rom", "slo", "swe", "hu", "cht", "vie"]
            }
        }
        self.active_service = "google"
        self.service_order = ["google", "deepl", "microsoft", "yandex", "baidu"]
    
    def get_service_info(self, service_name: str) -> Dict[str, Any]:
        """Get service information"""
        return self.services.get(service_name, {})
    
    def supports_capability(self, service_name: str, capability: int) -> bool:
        """Check if service supports a capability"""
        service = self.services.get(service_name, {})
        capabilities = service.get("capabilities", 0)
        return bool(capabilities & capability)
    
    def get_supported_languages(self, service_name: str) -> List[str]:
        """Get supported languages for a service"""
        service = self.services.get(service_name, {})
        return service.get("languages", [])

class AdvancedDictionaryManager:
    """Dictionary and definition lookup system"""
    
    def __init__(self):
        self.dictionary_services = {
            "oxford": {
                "name": "Oxford Learner Dictionary",
                "url_template": "https://www.oxfordlearnersdictionaries.com/definition/english/{word}",
                "languages": ["en"]
            },
            "cambridge": {
                "name": "Cambridge Dictionary",
                "url_template": "https://dictionary.cambridge.org/dictionary/english/{word}",
                "languages": ["en"]
            },
            "wordreference": {
                "name": "WordReference",
                "url_template": "https://www.wordreference.com/definition/{word}",
                "languages": ["en", "es", "fr", "it", "pt", "de"]
            }
        }
    
    def lookup_word(self, word: str, service: str = "oxford") -> str:
        """Look up word definition"""
        if service in self.dictionary_services:
            url = self.dictionary_services[service]["url_template"].format(word=quote(word))
            return url
        return ""

class SpeechManager:
    """Text-to-Speech and Speech-to-Text functionality"""
    
    def __init__(self):
        self.tts_enabled = True
        self.stt_enabled = True
        self.voice_speed = 1.0
        self.voice_language = "en"
    
    def speak_text(self, text: str, language: str = None):
        """Speak text using TTS"""
        if not self.tts_enabled:
            return
            
        try:
            # Placeholder for TTS functionality
            print(f"TTS: {text}")
        except Exception as e:
            print(f"TTS error: {e}")
    
    def start_speech_recognition(self, callback):
        """Start speech recognition"""
        if not self.stt_enabled:
            return
            
        try:
            # Placeholder for STT functionality
            callback("Speech recognition would be implemented here")
        except Exception as e:
            print(f"STT error: {e}")

class TranslationMemory:
    """翻譯記憶庫 - 靈感來自qTranslate-XT的內容管理"""
    def __init__(self, db_path="translation_memory.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化數據庫"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 創建翻譯記憶表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS translations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_text TEXT NOT NULL,
                target_text TEXT NOT NULL,
                source_lang TEXT NOT NULL,
                target_lang TEXT NOT NULL,
                provider TEXT NOT NULL,
                hash TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                used_count INTEGER DEFAULT 1
            )
        ''')
        
        # 創建多語言內容表（類似qTranslate-XT的多語言帖子）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS multilingual_content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_id TEXT NOT NULL,
                language TEXT NOT NULL,
                content TEXT NOT NULL,
                title TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(content_id, language)
            )
        ''')
        
        # 創建語言配置表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS language_config (
                code TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                native_name TEXT NOT NULL,
                enabled BOOLEAN DEFAULT 1,
                flag_url TEXT,
                rtl BOOLEAN DEFAULT 0
            )
        ''')
        
        # 初始化語言配置（在同一個連接中）
        self.init_language_config_data(cursor)
        
        conn.commit()
        conn.close()
    
    def init_language_config_data(self, cursor):
        """初始化語言配置數據 - 擴展qTranslate-XT的語言支持"""
        languages = [
            ('zh-CN', '简体中文', '简体中文', True, '', False),
            ('zh-TW', '繁體中文', '繁體中文', True, '', False),
            ('en', 'English', 'English', True, '', False),
            ('ja', '日本語', '日本語', True, '', False),
            ('ko', '한국어', '한국어', True, '', False),
            ('es', 'Español', 'Español', True, '', False),
            ('fr', 'Français', 'Français', True, '', False),
            ('de', 'Deutsch', 'Deutsch', True, '', False),
            ('it', 'Italiano', 'Italiano', True, '', False),
            ('pt', 'Português', 'Português', True, '', False),
            ('ru', 'Русский', 'Русский', True, '', False),
            ('ar', 'العربية', 'العربية', True, '', True),
            ('hi', 'हिन्दी', 'हिन्दी', True, '', False),
            ('th', 'ไทย', 'ไทย', True, '', False),
            ('vi', 'Tiếng Việt', 'Tiếng Việt', True, '', False),
        ]
        
        for lang in languages:
            cursor.execute('''
                INSERT OR IGNORE INTO language_config 
                (code, name, native_name, enabled, flag_url, rtl) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', lang)
    
    def get_translation(self, source_text: str, source_lang: str, target_lang: str) -> Optional[str]:
        """從記憶庫獲取翻譯"""
        text_hash = hashlib.md5(f"{source_text}{source_lang}{target_lang}".encode()).hexdigest()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT target_text FROM translations 
            WHERE hash = ? 
            ORDER BY used_count DESC, created_at DESC
            LIMIT 1
        ''', (text_hash,))
        
        result = cursor.fetchone()
        
        if result:
            # 增加使用計數
            cursor.execute('UPDATE translations SET used_count = used_count + 1 WHERE hash = ?', (text_hash,))
            conn.commit()
        
        conn.close()
        return result[0] if result else None
    
    def save_translation(self, source_text: str, target_text: str, source_lang: str, 
                        target_lang: str, provider: str):
        """保存翻譯到記憶庫"""
        text_hash = hashlib.md5(f"{source_text}{source_lang}{target_lang}".encode()).hexdigest()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO translations 
            (source_text, target_text, source_lang, target_lang, provider, hash) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (source_text, target_text, source_lang, target_lang, provider, text_hash))
        
        conn.commit()
        conn.close()
    
    def get_enabled_languages(self) -> List[Tuple[str, str, str]]:
        """獲取啟用的語言列表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT code, name, native_name FROM language_config 
                WHERE enabled = 1 
                ORDER BY name
            ''')
            result = cursor.fetchall()
        except sqlite3.OperationalError:
            # 如果表不存在，返回默認語言列表
            result = [
                ('zh-TW', '繁體中文', '繁體中文'),
                ('en', 'English', 'English'),
                ('ja', '日本語', '日本語'),
                ('ko', '한국어', '한국어'),
                ('es', 'Español', 'Español'),
                ('fr', 'Français', 'Français'),
                ('de', 'Deutsch', 'Deutsch'),
            ]
        
        conn.close()
        return result
    
    def save_multilingual_content(self, content_id: str, language: str, content: str, title: str = None):
        """保存多語言內容"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO multilingual_content 
            (content_id, language, content, title, updated_at) 
            VALUES (?, ?, ?, ?, ?)
        ''', (content_id, language, content, title, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()

class LanguageDetector:
    """語言檢測器"""
    def __init__(self):
        self.common_words = {
            'en': ['the', 'and', 'of', 'to', 'a', 'in', 'for', 'is', 'on', 'that'],
            'zh': ['的', '了', '是', '在', '我', '有', '和', '就', '不', '人'],
            'ja': ['の', 'に', 'は', 'を', 'た', 'が', 'で', 'て', 'と', 'し'],
            'ko': ['의', '가', '이', '은', '들', '는', '과', '도', '를', '로'],
            'es': ['de', 'la', 'que', 'el', 'en', 'y', 'a', 'es', 'se', 'no'],
            'fr': ['de', 'le', 'et', 'à', 'un', 'il', 'être', 'et', 'en', 'avoir'],
            'de': ['der', 'die', 'und', 'in', 'den', 'von', 'zu', 'das', 'mit', 'sich'],
            'ru': ['в', 'и', 'не', 'на', 'я', 'быть', 'то', 'он', 'с', 'а'],
        }
    
    def detect_language(self, text: str) -> str:
        """簡單的語言檢測"""
        if not text.strip():
            return 'auto'
        
        # 字符集檢測
        has_chinese = any('\u4e00' <= char <= '\u9fff' for char in text)
        has_japanese = any('\u3040' <= char <= '\u309f' or '\u30a0' <= char <= '\u30ff' for char in text)
        has_korean = any('\uac00' <= char <= '\ud7af' for char in text)
        has_arabic = any('\u0600' <= char <= '\u06ff' for char in text)
        has_cyrillic = any('\u0400' <= char <= '\u04ff' for char in text)
        
        if has_chinese and not has_japanese:
            return 'zh'
        elif has_japanese:
            return 'ja'
        elif has_korean:
            return 'ko'
        elif has_arabic:
            return 'ar'
        elif has_cyrillic:
            return 'ru'
        
        # 詞彙檢測
        words = text.lower().split()
        scores = {}
        
        for lang, common in self.common_words.items():
            score = sum(1 for word in words if word in common)
            if words:
                scores[lang] = score / len(words)
        
        if scores:
            detected = max(scores, key=scores.get)
            if scores[detected] > 0.1:  # 閾值
                return detected
        
        return 'auto'

class TranslationWorker(QThread):
    """翻譯工作線程 - 增強版支持記憶庫和語言檢測"""
    translation_complete = pyqtSignal(str)
    translation_error = pyqtSignal(str)
    
    def __init__(self, text, config, memory=None, source_lang='auto', target_lang=None):
        super().__init__()
        self.text = text
        self.config = config
        self.memory = memory
        self.source_lang = source_lang
        self.target_lang = target_lang or config.get('translation', {}).get('default_target', 'zh-TW')
        self.detector = LanguageDetector()  # 初始化語言檢測器
    
    def run(self):
        try:
            print(f"[DEBUG] TranslationWorker started for text: {self.text[:30]}...")
            
            # 自動檢測語言
            if self.source_lang == 'auto':
                try:
                    self.source_lang = self.detector.detect_language(self.text)
                    if self.source_lang == 'auto':
                        self.source_lang = 'en'  # 默認為英語
                except Exception as e:
                    print(f"[WARNING] Language detection failed: {e}, using 'en'")
                    self.source_lang = 'en'
            
            print(f"[DEBUG] Detected language: {self.source_lang} -> {self.target_lang}")
            
            # 檢查翻譯記憶庫
            if self.memory:
                try:
                    cached = self.memory.get_translation(self.text, self.source_lang, self.target_lang)
                    if cached:
                        print(f"[DEBUG] Using cached translation")
                        self.translation_complete.emit(cached)
                        return
                except Exception as e:
                    print(f"[WARNING] Memory lookup failed: {e}")
            
            print(f"[DEBUG] Starting translation...")
            result = self.translate_text(self.text)
            print(f"[DEBUG] Translation result: {result[:50] if result else 'None'}...")
            
            if not result:
                raise Exception("翻譯結果為空")
            
            # 保存到記憶庫
            if self.memory and result:
                try:
                    provider = self.config.get('translation_service', {}).get('provider', 'google')
                    self.memory.save_translation(self.text, result, self.source_lang, self.target_lang, provider)
                    print(f"[DEBUG] Saved to memory")
                except Exception as e:
                    print(f"[WARNING] Memory save failed: {e}")
            
            self.translation_complete.emit(result)
            print(f"[DEBUG] Translation complete signal emitted")
            
        except Exception as e:
            error_msg = f"翻譯失敗: {str(e)}"
            print(f"[ERROR] {error_msg}")
            self.translation_error.emit(error_msg)
    
    def translate_text(self, text):
        """根據配置選擇翻譯服務"""
        provider = self.config.get('translation_service', {}).get('provider', 'google')
        
        if provider == 'google':
            return self.translate_with_google(text)
        elif provider == 'custom_llm':
            return self.translate_with_custom_llm(text)
        else:
            return self.translate_with_google(text)  # 默認使用Google
    
    def translate_with_google(self, text):
        """使用Google翻譯API"""
        try:
            from googletrans import Translator
            translator = Translator()
            
            # 獲取目標語言，並映射到Google Translate支持的代碼
            target_lang = self.config.get('translation', {}).get('default_target', 'zh-TW')
            
            # 語言代碼映射
            language_mapping = {
                'zh-TW': 'zh-tw',  # 繁體中文
                'zh-CN': 'zh-cn',  # 簡體中文
                'zh': 'zh-cn',     # 默認簡體中文
                'en': 'en',        # 英語
                'ja': 'ja',        # 日語
                'ko': 'ko',        # 韓語
                'fr': 'fr',        # 法語
                'de': 'de',        # 德語
                'es': 'es',        # 西班牙語
                'pt': 'pt',        # 葡萄牙語
                'ru': 'ru',        # 俄語
                'ar': 'ar',        # 阿拉伯語
                'hi': 'hi',        # 印地語
                'th': 'th',        # 泰語
                'vi': 'vi'         # 越南語
            }
            
            # 使用映射的語言代碼，如果沒有映射則使用原始代碼
            google_lang_code = language_mapping.get(target_lang, target_lang)
            
            result = translator.translate(text, dest=google_lang_code)
            return result.text
        except ImportError:
            # 如果googletrans未安裝，使用備用方案
            return self.translate_with_requests(text)
        except Exception as e:
            raise Exception(f"Google翻譯錯誤: {str(e)}")
    
    def translate_with_requests(self, text):
        """使用requests直接調用Google翻譯API"""
        api_key = self.config.get('translation_service', {}).get('google_api', {}).get('api_key', '')
        if not api_key:
            raise Exception("Google API密鑰未設置")
        
        endpoint = self.config.get('translation_service', {}).get('google_api', {}).get('endpoint', '')
        target_lang = self.config.get('translation', {}).get('default_target', 'zh-TW')
        
        if target_lang == 'zh-TW':
            target_lang = 'zh'
        
        params = {
            'key': api_key,
            'q': text,
            'target': target_lang,
            'format': 'text'
        }
        
        response = requests.post(endpoint, data=params)
        if response.status_code == 200:
            result = response.json()
            return result['data']['translations'][0]['translatedText']
        else:
            raise Exception(f"API請求失敗: {response.status_code}")
    
    def translate_with_custom_llm(self, text):
        """使用自定義LLM翻譯"""
        llm_config = self.config.get('translation_service', {}).get('custom_llm', {})
        
        if not llm_config.get('enabled', False):
            raise Exception("自定義LLM未啟用")
        
        api_url = llm_config.get('api_url', '')
        api_key = llm_config.get('api_key', '')
        system_prompt = llm_config.get('system_prompt', '')
        
        if not api_url:
            raise Exception("LLM API URL未設置")
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        if api_key:
            headers['Authorization'] = f'Bearer {api_key}'
        
        # 構建請求數據（適用於OpenAI格式的API）
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"請翻譯以下文字：{text}"}
            ],
            "max_tokens": 1000,
            "temperature": 0.3
        }
        
        response = requests.post(api_url, json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            raise Exception(f"LLM API請求失敗: {response.status_code}")

class BatchTranslationWorker(QThread):
    """批量翻譯工作線程"""
    progress_updated = pyqtSignal(int, int)  # current, total
    translation_complete = pyqtSignal(list)  # list of results
    translation_error = pyqtSignal(str)
    
    def __init__(self, texts: List[str], source_lang: str, target_lang: str, config: dict, memory: TranslationMemory):
        super().__init__()
        self.texts = texts
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.config = config
        self.memory = memory
    
    def run(self):
        try:
            results = []
            total = len(self.texts)
            
            for i, text in enumerate(self.texts):
                # 先檢查翻譯記憶庫
                cached = self.memory.get_translation(text, self.source_lang, self.target_lang)
                if cached:
                    results.append({'original': text, 'translation': cached, 'source': 'cache'})
                else:
                    # 執行翻譯
                    worker = TranslationWorker(text, self.config)
                    translation = worker.translate_text(text)
                    
                    # 保存到記憶庫
                    provider = self.config.get('translation_service', {}).get('provider', 'google')
                    self.memory.save_translation(text, translation, self.source_lang, self.target_lang, provider)
                    
                    results.append({'original': text, 'translation': translation, 'source': 'api'})
                
                self.progress_updated.emit(i + 1, total)
                self.msleep(100)  # 避免API限制
            
            self.translation_complete.emit(results)
        except Exception as e:
            self.translation_error.emit(str(e))

class LanguageManagerDialog(QDialog):
    """語言管理對話框 - 類似qTranslate-XT的語言配置"""
    def __init__(self, memory: TranslationMemory, parent=None):
        super().__init__(parent)
        self.memory = memory
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("語言管理")
        self.setFixedSize(600, 400)
        
        layout = QVBoxLayout(self)
        
        # 語言列表
        self.language_table = QTableWidget()
        self.language_table.setColumnCount(4)
        self.language_table.setHorizontalHeaderLabels(['代碼', '語言名稱', '本地名稱', '啟用'])
        self.language_table.horizontalHeader().setStretchLastSection(True)
        
        self.load_languages()
        
        layout.addWidget(QLabel("語言配置:"))
        layout.addWidget(self.language_table)
        
        # 按鈕
        button_layout = QHBoxLayout()
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        save_button = QPushButton("保存")
        save_button.clicked.connect(self.save_languages)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
    
    def load_languages(self):
        """加載語言列表"""
        conn = sqlite3.connect(self.memory.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT code, name, native_name, enabled FROM language_config ORDER BY name')
        languages = cursor.fetchall()
        
        self.language_table.setRowCount(len(languages))
        
        for row, (code, name, native_name, enabled) in enumerate(languages):
            self.language_table.setItem(row, 0, QTableWidgetItem(code))
            self.language_table.setItem(row, 1, QTableWidgetItem(name))
            self.language_table.setItem(row, 2, QTableWidgetItem(native_name))
            
            enabled_checkbox = QCheckBox()
            enabled_checkbox.setChecked(bool(enabled))
            self.language_table.setCellWidget(row, 3, enabled_checkbox)
        
        conn.close()
    
    def save_languages(self):
        """保存語言配置"""
        conn = sqlite3.connect(self.memory.db_path)
        cursor = conn.cursor()
        
        for row in range(self.language_table.rowCount()):
            code = self.language_table.item(row, 0).text()
            enabled_checkbox = self.language_table.cellWidget(row, 3)
            enabled = enabled_checkbox.isChecked()
            
            cursor.execute('UPDATE language_config SET enabled = ? WHERE code = ?', (enabled, code))
        
        conn.commit()
        conn.close()
        
        QMessageBox.information(self, "成功", "語言配置已保存！")
        self.accept()

class BatchTranslationDialog(QDialog):
    """批量翻譯對話框"""
    def __init__(self, config: dict, memory: TranslationMemory, parent=None):
        super().__init__(parent)
        self.config = config
        self.memory = memory
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("批量翻譯")
        self.setFixedSize(800, 600)
        
        layout = QVBoxLayout(self)
        
        # 語言選擇
        lang_layout = QHBoxLayout()
        
        lang_layout.addWidget(QLabel("源語言:"))
        self.source_combo = QComboBox()
        self.source_combo.addItem("自動檢測", "auto")
        for code, name, native in self.memory.get_enabled_languages():
            self.source_combo.addItem(f"{name} ({native})", code)
        lang_layout.addWidget(self.source_combo)
        
        lang_layout.addWidget(QLabel("目標語言:"))
        self.target_combo = QComboBox()
        for code, name, native in self.memory.get_enabled_languages():
            self.target_combo.addItem(f"{name} ({native})", code)
        lang_layout.addWidget(self.target_combo)
        
        layout.addLayout(lang_layout)
        
        # 輸入區域
        input_group = QGroupBox("待翻譯文本")
        input_layout = QVBoxLayout(input_group)
        
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("請輸入待翻譯的文本，每行一個條目...")
        input_layout.addWidget(self.input_text)
        
        layout.addWidget(input_group)
        
        # 進度條
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # 結果區域
        result_group = QGroupBox("翻譯結果")
        result_layout = QVBoxLayout(result_group)
        
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(['原文', '譯文', '來源'])
        self.result_table.horizontalHeader().setStretchLastSection(True)
        result_layout.addWidget(self.result_table)
        
        layout.addWidget(result_group)
        
        # 按鈕
        button_layout = QHBoxLayout()
        
        self.translate_button = QPushButton("開始翻譯")
        self.translate_button.clicked.connect(self.start_translation)
        
        export_button = QPushButton("導出結果")
        export_button.clicked.connect(self.export_results)
        
        clear_button = QPushButton("清空")
        clear_button.clicked.connect(self.clear_all)
        
        close_button = QPushButton("關閉")
        close_button.clicked.connect(self.accept)
        
        button_layout.addWidget(self.translate_button)
        button_layout.addWidget(export_button)
        button_layout.addWidget(clear_button)
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
    
    def start_translation(self):
        """開始批量翻譯"""
        text_content = self.input_text.toPlainText().strip()
        if not text_content:
            QMessageBox.warning(self, "警告", "請輸入待翻譯的文本！")
            return
        
        texts = [line.strip() for line in text_content.split('\n') if line.strip()]
        if not texts:
            QMessageBox.warning(self, "警告", "沒有有效的文本行！")
            return
        
        source_lang = self.source_combo.currentData()
        target_lang = self.target_combo.currentData()
        
        self.translate_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(texts))
        self.progress_bar.setValue(0)
        
        # 啟動批量翻譯線程
        self.batch_worker = BatchTranslationWorker(texts, source_lang, target_lang, self.config, self.memory)
        self.batch_worker.progress_updated.connect(self.update_progress)
        self.batch_worker.translation_complete.connect(self.show_results)
        self.batch_worker.translation_error.connect(self.show_error)
        self.batch_worker.start()
    
    def update_progress(self, current, total):
        """更新進度"""
        self.progress_bar.setValue(current)
    
    def show_results(self, results):
        """顯示翻譯結果"""
        self.result_table.setRowCount(len(results))
        
        for row, result in enumerate(results):
            self.result_table.setItem(row, 0, QTableWidgetItem(result['original']))
            self.result_table.setItem(row, 1, QTableWidgetItem(result['translation']))
            
            source_text = "緩存" if result['source'] == 'cache' else "API"
            self.result_table.setItem(row, 2, QTableWidgetItem(source_text))
        
        self.progress_bar.setVisible(False)
        self.translate_button.setEnabled(True)
        
        QMessageBox.information(self, "完成", f"成功翻譯 {len(results)} 個條目！")
    
    def show_error(self, error):
        """顯示錯誤"""
        self.progress_bar.setVisible(False)
        self.translate_button.setEnabled(True)
        QMessageBox.critical(self, "錯誤", f"翻譯失敗：{error}")
    
    def export_results(self):
        """導出結果"""
        if self.result_table.rowCount() == 0:
            QMessageBox.warning(self, "警告", "沒有結果可導出！")
            return
        
        # 簡單的文本導出
        results = []
        for row in range(self.result_table.rowCount()):
            original = self.result_table.item(row, 0).text()
            translation = self.result_table.item(row, 1).text()
            results.append(f"{original}\t{translation}")
        
        export_text = "\n".join(results)
        pyperclip.copy(export_text)
        QMessageBox.information(self, "成功", "結果已複製到剪貼板！")
    
    def clear_all(self):
        """清空所有內容"""
        self.input_text.clear()
        self.result_table.setRowCount(0)

class TranslationHistoryDialog(QDialog):
    """翻譯歷史對話框"""
    def __init__(self, memory: TranslationMemory, parent=None):
        super().__init__(parent)
        self.memory = memory
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("翻譯歷史")
        self.setFixedSize(900, 600)
        
        layout = QVBoxLayout(self)
        
        # 搜索區域
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("搜索:"))
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("輸入關鍵詞搜索...")
        self.search_input.textChanged.connect(self.search_translations)
        search_layout.addWidget(self.search_input)
        
        layout.addLayout(search_layout)
        
        # 歷史表格
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels(['原文', '譯文', '源語言', '目標語言', '提供商', '使用次數'])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.history_table)
        
        # 按鈕
        button_layout = QHBoxLayout()
        
        refresh_button = QPushButton("刷新")
        refresh_button.clicked.connect(self.load_history)
        
        clear_button = QPushButton("清空歷史")
        clear_button.clicked.connect(self.clear_history)
        
        close_button = QPushButton("關閉")
        close_button.clicked.connect(self.accept)
        
        button_layout.addWidget(refresh_button)
        button_layout.addWidget(clear_button)
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        # 加載歷史
        self.load_history()
    
    def load_history(self):
        """加載翻譯歷史"""
        conn = sqlite3.connect(self.memory.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT source_text, target_text, source_lang, target_lang, provider, used_count 
            FROM translations 
            ORDER BY used_count DESC, created_at DESC 
            LIMIT 1000
        ''')
        
        translations = cursor.fetchall()
        
        self.history_table.setRowCount(len(translations))
        
        for row, (source, target, src_lang, tgt_lang, provider, count) in enumerate(translations):
            self.history_table.setItem(row, 0, QTableWidgetItem(source[:100] + "..." if len(source) > 100 else source))
            self.history_table.setItem(row, 1, QTableWidgetItem(target[:100] + "..." if len(target) > 100 else target))
            self.history_table.setItem(row, 2, QTableWidgetItem(src_lang))
            self.history_table.setItem(row, 3, QTableWidgetItem(tgt_lang))
            self.history_table.setItem(row, 4, QTableWidgetItem(provider))
            self.history_table.setItem(row, 5, QTableWidgetItem(str(count)))
        
        conn.close()
    
    def search_translations(self, text):
        """搜索翻譯"""
        if not text:
            self.load_history()
            return
        
        conn = sqlite3.connect(self.memory.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT source_text, target_text, source_lang, target_lang, provider, used_count 
            FROM translations 
            WHERE source_text LIKE ? OR target_text LIKE ?
            ORDER BY used_count DESC, created_at DESC 
            LIMIT 500
        ''', (f'%{text}%', f'%{text}%'))
        
        translations = cursor.fetchall()
        
        self.history_table.setRowCount(len(translations))
        
        for row, (source, target, src_lang, tgt_lang, provider, count) in enumerate(translations):
            self.history_table.setItem(row, 0, QTableWidgetItem(source[:100] + "..." if len(source) > 100 else source))
            self.history_table.setItem(row, 1, QTableWidgetItem(target[:100] + "..." if len(target) > 100 else target))
            self.history_table.setItem(row, 2, QTableWidgetItem(src_lang))
            self.history_table.setItem(row, 3, QTableWidgetItem(tgt_lang))
            self.history_table.setItem(row, 4, QTableWidgetItem(provider))
            self.history_table.setItem(row, 5, QTableWidgetItem(str(count)))
        
        conn.close()
    
    def clear_history(self):
        """清空翻譯歷史"""
        reply = QMessageBox.question(self, "確認", "確定要清空所有翻譯歷史嗎？此操作不可撤銷。",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            conn = sqlite3.connect(self.memory.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM translations')
            conn.commit()
            conn.close()
            
            self.load_history()
            QMessageBox.information(self, "成功", "翻譯歷史已清空！")

class SettingsDialog(QDialog):
    """設置對話框"""
    def __init__(self, config, translation_memory=None, parent=None):
        super().__init__(parent)
        self.config = config.copy()  # 創建配置的副本
        self.translation_memory = translation_memory  # 使用現有的翻譯記憶庫實例
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("翻譯器設置")
        self.setFixedSize(600, 500)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        layout = QVBoxLayout(self)
        
        # 創建標籤頁
        tab_widget = QTabWidget()
        
        # 翻譯服務標籤頁
        translation_tab = self.create_translation_tab()
        tab_widget.addTab(translation_tab, "翻譯服務")
        
        # 自定義LLM標籤頁
        llm_tab = self.create_llm_tab()
        tab_widget.addTab(llm_tab, "自定義LLM")
        
        # 一般設置標籤頁
        general_tab = self.create_general_tab()
        tab_widget.addTab(general_tab, "一般設置")
        
        layout.addWidget(tab_widget)
        
        # 按鈕區域
        button_layout = QHBoxLayout()
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        save_button = QPushButton("儲存")
        save_button.clicked.connect(self.save_config)
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
    
    def create_translation_tab(self):
        """創建翻譯服務設置標籤"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        # 翻譯服務提供商選擇
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["Google翻譯", "自定義LLM"])
        
        current_provider = self.config.get('translation_service', {}).get('provider', 'google')
        if current_provider == 'google':
            self.provider_combo.setCurrentText("Google翻譯")
        else:
            self.provider_combo.setCurrentText("自定義LLM")
        
        layout.addRow("翻譯服務:", self.provider_combo)
        
        # 語言管理按鈕
        lang_button = QPushButton("管理語言")
        lang_button.clicked.connect(self.open_language_manager)
        layout.addRow("語言設置:", lang_button)
        
        # Google API設置
        google_group = QWidget()
        google_layout = QFormLayout(google_group)
        
        self.google_api_key = QLineEdit()
        self.google_api_key.setEchoMode(QLineEdit.Password)
        self.google_api_key.setText(
            self.config.get('translation_service', {}).get('google_api', {}).get('api_key', '')
        )
        google_layout.addRow("Google API 密鑰:", self.google_api_key)
        
        self.google_endpoint = QLineEdit()
        self.google_endpoint.setText(
            self.config.get('translation_service', {}).get('google_api', {}).get('endpoint', 
            'https://translation.googleapis.com/language/translate/v2')
        )
        google_layout.addRow("API 端點:", self.google_endpoint)
        
        layout.addRow("Google翻譯設置:", google_group)
        
        # 目標語言設置
        self.target_lang_combo = QComboBox()
        self.target_lang_combo.addItems([
            "繁體中文 (zh-TW)", "簡體中文 (zh-CN)", "英文 (en)", 
            "日文 (ja)", "韓文 (ko)", "法文 (fr)", "德文 (de)", "西班牙文 (es)"
        ])
        
        current_target = self.config.get('translation', {}).get('default_target', 'zh-TW')
        lang_map = {
            'zh-TW': 0, 'zh-CN': 1, 'en': 2, 'ja': 3, 
            'ko': 4, 'fr': 5, 'de': 6, 'es': 7
        }
        self.target_lang_combo.setCurrentIndex(lang_map.get(current_target, 0))
        
        layout.addRow("預設目標語言:", self.target_lang_combo)
        
        return widget
    
    def create_llm_tab(self):
        """創建自定義LLM設置標籤"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        # 啟用自定義LLM
        self.llm_enabled = QCheckBox("啟用自定義LLM")
        self.llm_enabled.setChecked(
            self.config.get('translation_service', {}).get('custom_llm', {}).get('enabled', False)
        )
        layout.addRow("", self.llm_enabled)
        
        # API URL
        self.llm_url = QLineEdit()
        self.llm_url.setText(
            self.config.get('translation_service', {}).get('custom_llm', {}).get('api_url', '')
        )
        self.llm_url.setPlaceholderText("例如: https://api.openai.com/v1/chat/completions")
        layout.addRow("API URL:", self.llm_url)
        
        # API 密鑰
        self.llm_api_key = QLineEdit()
        self.llm_api_key.setEchoMode(QLineEdit.Password)
        self.llm_api_key.setText(
            self.config.get('translation_service', {}).get('custom_llm', {}).get('api_key', '')
        )
        layout.addRow("API 密鑰:", self.llm_api_key)
        
        # 系統提示詞
        self.system_prompt = QTextEdit()
        self.system_prompt.setMaximumHeight(100)
        default_prompt = self.config.get('translation_service', {}).get('custom_llm', {}).get('system_prompt', 
            'You are a professional translator. Translate the following text accurately while preserving the original meaning and context. Only provide the translation without any additional explanation.')
        self.system_prompt.setPlainText(default_prompt)
        layout.addRow("系統提示詞:", self.system_prompt)
        
        # 說明文字
        info_label = QLabel("提示：自定義LLM應該支援OpenAI相容的API格式")
        info_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addRow("", info_label)
        
        return widget
    
    def create_general_tab(self):
        """創建一般設置標籤"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        # 自動翻譯
        self.auto_translate = QCheckBox("自動翻譯")
        self.auto_translate.setChecked(
            self.config.get('translation', {}).get('auto_translate', True)
        )
        layout.addRow("", self.auto_translate)
        
        # 保持格式
        self.preserve_format = QCheckBox("保持原文格式")
        self.preserve_format.setChecked(
            self.config.get('translation', {}).get('preserve_format', True)
        )
        layout.addRow("", self.preserve_format)
        
        # 字體大小
        self.font_size = QComboBox()
        self.font_size.addItems(["10", "12", "14", "16", "18", "20"])
        current_size = str(self.config.get('ui', {}).get('font_size', 14))
        self.font_size.setCurrentText(current_size)
        layout.addRow("字體大小:", self.font_size)
        
        # 視窗透明度
        self.opacity = QComboBox()
        self.opacity.addItems(["70%", "80%", "90%", "95%", "100%"])
        current_opacity = self.config.get('ui', {}).get('window_opacity', 0.95)
        opacity_map = {0.7: 0, 0.8: 1, 0.9: 2, 0.95: 3, 1.0: 4}
        self.opacity.setCurrentIndex(opacity_map.get(current_opacity, 3))
        layout.addRow("視窗透明度:", self.opacity)
        
        return widget
    
    def save_config(self):
        """儲存配置"""
        try:
            # 更新翻譯服務設置
            if self.provider_combo.currentText() == "Google翻譯":
                self.config['translation_service']['provider'] = 'google'
            else:
                self.config['translation_service']['provider'] = 'custom_llm'
            
            # 更新Google API設置
            self.config['translation_service']['google_api']['api_key'] = self.google_api_key.text()
            self.config['translation_service']['google_api']['endpoint'] = self.google_endpoint.text()
            
            # 更新自定義LLM設置
            self.config['translation_service']['custom_llm']['enabled'] = self.llm_enabled.isChecked()
            self.config['translation_service']['custom_llm']['api_url'] = self.llm_url.text()
            self.config['translation_service']['custom_llm']['api_key'] = self.llm_api_key.text()
            self.config['translation_service']['custom_llm']['system_prompt'] = self.system_prompt.toPlainText()
            
            # 更新目標語言
            lang_values = ['zh-TW', 'zh-CN', 'en', 'ja', 'ko', 'fr', 'de', 'es']
            self.config['translation']['default_target'] = lang_values[self.target_lang_combo.currentIndex()]
            
            # 更新一般設置
            self.config['translation']['auto_translate'] = self.auto_translate.isChecked()
            self.config['translation']['preserve_format'] = self.preserve_format.isChecked()
            self.config['ui']['font_size'] = int(self.font_size.currentText())
            
            opacity_values = [0.7, 0.8, 0.9, 0.95, 1.0]
            self.config['ui']['window_opacity'] = opacity_values[self.opacity.currentIndex()]
            
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"儲存設置時出錯：{str(e)}")
    
    def open_language_manager(self):
        """打開語言管理對話框"""
        # 使用現有的翻譯記憶庫實例，如果沒有則創建新的
        if self.translation_memory:
            dialog = LanguageManagerDialog(self.translation_memory, self)
        else:
            # 如果沒有傳入翻譯記憶庫，創建臨時實例
            temp_memory = TranslationMemory()
            dialog = LanguageManagerDialog(temp_memory, self)
        dialog.exec_()

class TranslatorWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 防止窗口關閉時退出應用程序
        self.setAttribute(Qt.WA_QuitOnClose, False)
        self.auto_hide_timer = QTimer()
        self.auto_hide_timer.timeout.connect(self.fade_out)
        self.initUI()
        
    def initUI(self):
        # 設置窗口屬性
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool |  # 防止在任務欄顯示
            Qt.WindowDoesNotAcceptFocus  # 防止搶奪焦點
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)  # 顯示時不激活
        
        # 設置固定大小
        self.setFixedSize(350, 120)
        
        # 創建主容器
        main_widget = QWidget()
        main_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.95);
                border: 1px solid #d0d0d0;
                border-radius: 8px;
            }
        """)
        
        # 添加陰影效果
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(Qt.black)
        shadow.setOffset(0, 2)
        main_widget.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 內容布局
        content_layout = QVBoxLayout(main_widget)
        content_layout.setContentsMargins(15, 10, 15, 10)
        content_layout.setSpacing(8)
        
        # 翻譯結果顯示區域
        self.result_label = QLabel()
        self.result_label.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border: none;
                font-size: 13px;
                color: #333;
                padding: 5px;
            }
        """)
        self.result_label.setWordWrap(True)
        self.result_label.setAlignment(Qt.AlignTop)
        content_layout.addWidget(self.result_label)
        
        # 按鈕區域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
        # 複製按鈕
        self.copy_button = QPushButton("📋 複製")
        self.copy_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.copy_button.clicked.connect(self.copy_translation)
        button_layout.addWidget(self.copy_button)
        
        # 關閉按鈕
        close_button = QPushButton("✕")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 8px;
                font-size: 11px;
                font-weight: bold;
                max-width: 30px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #c1170a;
            }
        """)
        close_button.clicked.connect(self.fade_out)
        button_layout.addWidget(close_button)
        
        content_layout.addLayout(button_layout)
        layout.addWidget(main_widget)
        self.setLayout(layout)
        
    def copy_translation(self):
        """複製翻譯結果到剪貼板"""
        # 提取純文本（去除"翻譯結果："前綴）
        text = self.result_label.text()
        if text.startswith("翻譯結果："):
            text = text[5:]  # 移除前綴
        elif text.startswith("翻譯錯誤："):
            text = text[5:]  # 移除錯誤前綴
        
        pyperclip.copy(text)
        
        # 顯示複製成功反饋
        original_text = self.copy_button.text()
        self.copy_button.setText("✓ 已複製")
        self.copy_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 11px;
                font-weight: bold;
            }
        """)
        
        # 恢復原始文本
        QTimer.singleShot(1000, lambda: self.restore_copy_button(original_text))
        
    def restore_copy_button(self, original_text):
        """恢復複製按鈕原始狀態"""
        self.copy_button.setText(original_text)
        self.copy_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        
    def show_translation(self, text, translation):
        """顯示翻譯結果 - 安全版本避免視窗錯誤"""
        print(f"[DEBUG] *** SHOW_TRANSLATION CALLED *** Text: {text[:30] if text else 'None'}... Translation: {translation[:50] if translation else 'None'}...")
        
        try:
            # 自動複製翻譯結果到剪貼簿
            try:
                import pyperclip
                pyperclip.copy(translation)
                print(f"[SUCCESS] Translation copied to clipboard: {translation[:50]}...")
            except Exception as clipboard_error:
                print(f"[WARNING] Failed to copy to clipboard: {clipboard_error}")
            
            # 檢查是否已經有有效的視窗
            if not self.isValid():
                print("[WARNING] Window handle is invalid, recreating...")
                self.initUI()
            
            # 設置翻譯結果 - 簡化版本
            display_text = f"原文: {text}\n\n翻譯: {translation}\n\n✅ 已複製到剪貼簿"
            self.result_label.setText(display_text)
            
            # 簡單樣式
            self.result_label.setStyleSheet("""
                QLabel {
                    background-color: #f0f0f0;
                    border: 2px solid #333;
                    font-size: 16px;
                    color: #000;
                    padding: 15px;
                    font-weight: bold;
                }
            """)
            
            # 安全的視窗顯示方式
            try:
                # 設置基本視窗屬性
                self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
                self.setAttribute(Qt.WA_ShowWithoutActivating, True)
                
                # 調整大小並顯示
                self.adjustSize()
                self.show()
                
                # 嘗試提升視窗層級
                try:
                    self.raise_()
                    self.activateWindow()
                except Exception as raise_error:
                    print(f"[WARNING] Failed to raise window: {raise_error}")
                
                print(f"[SUCCESS] *** TRANSLATION WINDOW SHOULD BE VISIBLE NOW ***")
                
                # 設置自動隱藏定時器（15秒）
                if hasattr(self, 'auto_hide_timer'):
                    self.auto_hide_timer.start(15000)
                else:
                    # 創建定時器如果不存在
                    self.auto_hide_timer = QTimer()
                    self.auto_hide_timer.timeout.connect(self.fade_out)
                    self.auto_hide_timer.start(15000)
                
            except Exception as window_error:
                print(f"[ERROR] Window display error: {window_error}")
                # 降級到簡單顯示
                try:
                    self.setWindowFlags(Qt.Window)
                    self.show()
                    print("[INFO] Fallback window display successful")
                except Exception as fallback_error:
                    print(f"[ERROR] Fallback window display failed: {fallback_error}")
            
        except Exception as e:
            print(f"[ERROR] Error in show_translation: {e}")
            import traceback
            traceback.print_exc()
    
    def isValid(self):
        """檢查視窗控制代碼是否有效"""
        try:
            # 簡單檢查視窗是否可用
            return self.winId() != 0 and not self.isHidden()
        except Exception:
            return False
        
    def show_error(self, error):
        """顯示錯誤訊息"""
        self.result_label.setText(f"{error}")
        self.result_label.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border: none;
                font-size: 13px;
                color: #c62828;
                padding: 5px;
            }
        """)
        # 錯誤訊息顯示較短時間（5秒）
        self.auto_hide_timer.start(5000)
        
    def show_at_position(self, pos):
        """在指定位置顯示窗口"""
        try:
            # 停止自動隱藏定時器
            self.auto_hide_timer.stop()
            
            # 獲取當前鼠標所在的屏幕
            desktop = QApplication.desktop()
            screen_num = desktop.screenNumber(pos)
            screen_geometry = desktop.screenGeometry(screen_num)
            
            # 計算窗口位置（鼠標右下方，留出距離避免遮擋）
            x = pos.x() + 20
            y = pos.y() + 20
            
            # 確保窗口不會超出屏幕邊界
            if x + self.width() > screen_geometry.right():
                x = pos.x() - self.width() - 20  # 顯示在鼠標左邊
            if y + self.height() > screen_geometry.bottom():
                y = pos.y() - self.height() - 20  # 顯示在鼠標上方
                
            # 最終邊界檢查
            x = max(screen_geometry.left(), min(x, screen_geometry.right() - self.width()))
            y = max(screen_geometry.top(), min(y, screen_geometry.bottom() - self.height()))
            
            self.move(x, y)
            self.show()
            self.raise_()
            
        except Exception as e:
            print(f"Error showing translator window: {e}")
            # 如果位置計算失敗，顯示在主屏幕中央
            screen = QApplication.desktop().screenGeometry()
            self.move(
                screen.center().x() - self.width() // 2,
                screen.center().y() - self.height() // 2
            )
            self.show()
    
    def fade_out(self):
        """淡出隱藏窗口 - 安全版本"""
        try:
            if hasattr(self, 'auto_hide_timer') and self.auto_hide_timer.isActive():
                self.auto_hide_timer.stop()
            
            # 安全隱藏視窗
            if self.isVisible():
                self.hide()
                print("[INFO] Translation window hidden")
        except Exception as e:
            print(f"[WARNING] Error in fade_out: {e}")
            # 強制隱藏
            try:
                self.hide()
            except Exception:
                pass
        
    def enterEvent(self, event):
        """鼠標進入時停止自動隱藏"""
        self.auto_hide_timer.stop()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        """鼠標離開時重新開始自動隱藏倒計時"""
        self.auto_hide_timer.start(3000)  # 3秒後隱藏
        super().leaveEvent(event)

class TranslatorApp(QObject):
    # 添加信號用於線程安全的通信
    text_copied = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        # 設置應用程序不要在最後一個窗口關閉時退出（系統托盤應用）
        self.app.setQuitOnLastWindowClosed(False)
        self.translator_window = TranslatorWindow()
        self.translation_memory = TranslationMemory()  # 初始化翻譯記憶庫
        
        # QTranslate-inspired advanced features
        self.theme_manager = ThemeManager()
        self.hotkey_manager = AdvancedHotkeyManager(self)
        self.ocr_translator = OCRTranslator()
        self.multi_service_translator = MultiServiceTranslator()
        self.dictionary_manager = AdvancedDictionaryManager()
        self.speech_manager = SpeechManager()
        
        # Advanced state management
        self.mouse_mode = QTranslateAdvancedFeatures.MOUSE_MODE_ICON_SHOW
        self.instant_translation = False
        self.auto_detect_language = True
        self.selected_text_history = []
        self.current_translation_index = 0
        self.exception_list = []  # Apps/windows to ignore
        
        # Enhanced configuration
        self.popup_timeout = QTranslateAdvancedFeatures.DEFAULT_POPUP_TIMEOUT
        self.popup_auto_position = True
        self.popup_auto_size = True
        self.transparency = 0.95
        self.enable_history = True
        self.clear_history_on_exit = False
        
        # Service management
        self.active_services = ["google"]
        self.service_order = ["google", "deepl", "microsoft", "yandex", "baidu"]
        self.active_dictionary_services = ["oxford"]
        
        self.load_config()
        
        # Apply current theme
        self.apply_theme()
        
        self.setup_tray()
        self.setup_hotkeys()
        self.translation_worker = None
        
        # 連接信號到槽
        self.text_copied.connect(self.handle_copied_text)
        
    def load_config(self):
        """載入配置文件"""
        try:
            config_path = resource_path('config.json')
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = {}
    
    def save_config(self):
        """儲存配置文件"""
        try:
            config_path = resource_path('config.json')
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")
        
    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon()
        icon_path = resource_path('icon.png')
        self.tray_icon.setIcon(QIcon(icon_path))
        
        # 創建托盤菜單
        tray_menu = QMenu()
        
        # 添加自動翻譯開關
        self.auto_translate_action = QAction("✓ 自動翻譯", self.app)
        self.auto_translate_action.setCheckable(True)
        self.auto_translate_action.setChecked(self.config.get('translation', {}).get('auto_translate', True))
        self.auto_translate_action.triggered.connect(self.toggle_auto_translate)
        tray_menu.addAction(self.auto_translate_action)
        
        # 添加分隔線
        tray_menu.addSeparator()
        
        # 添加設置選項
        settings_action = QAction("設置", self.app)
        settings_action.triggered.connect(self.show_settings)
        tray_menu.addAction(settings_action)
        
        # 添加批量翻譯選項
        batch_action = QAction("批量翻譯", self.app)
        batch_action.triggered.connect(self.show_batch_translation)
        tray_menu.addAction(batch_action)
        
        # 添加翻譯歷史選項
        history_action = QAction("翻譯歷史", self.app)
        history_action.triggered.connect(self.show_translation_history)
        tray_menu.addAction(history_action)
        
        # 添加語言管理選項
        language_action = QAction("語言管理", self.app)
        language_action.triggered.connect(self.show_language_manager)
        tray_menu.addAction(language_action)
        
        # 添加分隔線
        tray_menu.addSeparator()
        
        # 添加測試翻譯選項
        test_action = QAction("🧪 測試翻譯", self.app)
        test_action.triggered.connect(self.test_translation)
        tray_menu.addAction(test_action)
        
        # 添加手動翻譯選項
        manual_action = QAction("手動翻譯 (Ctrl+Shift+T)", self.app)
        manual_action.triggered.connect(self.manual_translate)
        tray_menu.addAction(manual_action)
        
        # 添加分隔線
        tray_menu.addSeparator()
        
        # 添加退出選項
        exit_action = QAction("退出", self.app)
        exit_action.triggered.connect(self.app.quit)
        tray_menu.addAction(exit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        # 添加托盤圖標點擊事件
        self.tray_icon.activated.connect(self.tray_icon_activated)
    
    def tray_icon_activated(self, reason):
        """托盤圖標點擊事件"""
        if reason == QSystemTrayIcon.DoubleClick:
            # 雙擊打開設置
            self.show_settings()
        elif reason == QSystemTrayIcon.Trigger:
            # 單擊顯示狀態信息
            auto_enabled = self.config.get('translation', {}).get('auto_translate', True)
            status = "啟用" if auto_enabled else "禁用"
            self.tray_icon.showMessage(
                "LLM翻譯器", 
                f"自動翻譯: {status}\n雙擊打開設置，右鍵查看菜單", 
                QSystemTrayIcon.Information, 
                2000
            )
    
    def toggle_auto_translate(self):
        """切換自動翻譯狀態"""
        current_state = self.config.get('translation', {}).get('auto_translate', True)
        new_state = not current_state
        
        # 更新配置
        if 'translation' not in self.config:
            self.config['translation'] = {}
        self.config['translation']['auto_translate'] = new_state
        self.save_config()
        
        # 更新菜單項
        self.auto_translate_action.setChecked(new_state)
        if new_state:
            self.auto_translate_action.setText("✓ 自動翻譯")
        else:
            self.auto_translate_action.setText("✗ 自動翻譯")
        
        # 顯示通知
        status = "啟用" if new_state else "禁用"
        self.tray_icon.showMessage(
            "LLM翻譯器", 
            f"自動翻譯已{status}！\n{'現在會在複製文字時自動翻譯' if new_state else '使用 Ctrl+Shift+T 手動翻譯'}", 
            QSystemTrayIcon.Information, 
            3000
        )
    
    def manual_translate(self):
        """手動翻譯剪貼板內容"""
        try:
            text = pyperclip.paste().strip()
            if text:
                cursor_pos = QCursor.pos()
                self.start_translation(text, cursor_pos)
            else:
                self.tray_icon.showMessage(
                    "LLM翻譯器", 
                    "剪貼板沒有文本內容！", 
                    QSystemTrayIcon.Warning, 
                    2000
                )
        except Exception as e:
            print(f"Manual translation error: {e}")
            self.tray_icon.showMessage(
                "LLM翻譯器", 
                f"手動翻譯失敗：{str(e)}", 
                QSystemTrayIcon.Critical, 
                3000
            )
        
    def show_settings(self):
        """顯示設置對話框"""
        try:
            # 創建一個不可見的父窗口來防止應用程序退出
            settings_dialog = SettingsDialog(self.config, self.translation_memory, None)
            # 設置對話框屬性，防止關閉時退出應用
            settings_dialog.setAttribute(Qt.WA_QuitOnClose, False)
            if settings_dialog.exec_() == QDialog.Accepted:
                self.config = settings_dialog.config
                self.save_config()
        except Exception as e:
            print(f"Error opening settings dialog: {e}")
            # 顯示錯誤消息給用戶
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(None, "錯誤", f"設置對話框打開失敗：{str(e)}")
    
    def show_batch_translation(self):
        """顯示批量翻譯對話框"""
        try:
            batch_dialog = BatchTranslationDialog(self.config, self.translation_memory, None)
            batch_dialog.setAttribute(Qt.WA_QuitOnClose, False)
            batch_dialog.exec_()
        except Exception as e:
            print(f"Error opening batch translation dialog: {e}")
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(None, "錯誤", f"批量翻譯對話框打開失敗：{str(e)}")
    
    def show_translation_history(self):
        """顯示翻譯歷史對話框"""
        try:
            history_dialog = TranslationHistoryDialog(self.translation_memory, None)
            history_dialog.setAttribute(Qt.WA_QuitOnClose, False)
            history_dialog.exec_()
        except Exception as e:
            print(f"Error opening translation history dialog: {e}")
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(None, "錯誤", f"翻譯歷史對話框打開失敗：{str(e)}")
    
    def show_language_manager(self):
        """顯示語言管理對話框"""
        try:
            language_dialog = LanguageManagerDialog(self.translation_memory, None)
            language_dialog.setAttribute(Qt.WA_QuitOnClose, False)
            language_dialog.exec_()
        except Exception as e:
            print(f"Error opening language manager dialog: {e}")
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(None, "錯誤", f"語言管理對話框打開失敗：{str(e)}")
        
    def setup_hotkeys(self):
        """Setup comprehensive QTranslate-inspired hotkeys with safe fallback"""
        self.hotkeys_enabled = False
        
        # Check if running as administrator
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if not is_admin:
                print("[WARNING] Not running as administrator - some hotkeys may fail")
        except Exception:
            print("[WARNING] Cannot check administrator privileges")
        
        try:
            # Import keyboard library and test basic functionality
            import keyboard
            
            # Test if keyboard library works without causing access violations
            print("[INFO] Testing keyboard library compatibility...")
            
            # Clear any existing hotkeys safely
            try:
                keyboard.unhook_all()
                time.sleep(0.1)  # Give time for cleanup
            except Exception as e:
                print(f"[WARNING] Failed to clear existing hotkeys: {e}")
            
            # Test basic keyboard functionality with timeout
            def test_hotkey_function():
                print("[DEBUG] Test hotkey triggered")
            
            # Register a test hotkey first with safer parameters
            try:
                test_hotkey = keyboard.add_hotkey('ctrl+shift+f12', test_hotkey_function, suppress=False)
                time.sleep(0.2)  # Wait for registration
                
                # If we get here without error, keyboard library works
                keyboard.remove_hotkey(test_hotkey)
                time.sleep(0.1)  # Give time for cleanup
                
                # Register QTranslate-inspired hotkeys with safer settings
                print("[INFO] Registering QTranslate hotkeys...")
                
                # Core translation hotkeys - use suppress=False to avoid access violations
                keyboard.add_hotkey('ctrl+q', self.show_popup_translation, suppress=False)
                keyboard.add_hotkey('ctrl+shift+q', self.web_search_selection, suppress=False)
                keyboard.add_hotkey('ctrl+shift+t', self.manual_translate, suppress=False)
                keyboard.add_hotkey('ctrl+e', self.listen_selected_text, suppress=False)
                keyboard.add_hotkey('ctrl+d', self.show_dictionary, suppress=False)
                keyboard.add_hotkey('ctrl+i', self.switch_languages, suppress=False)
                keyboard.add_hotkey('ctrl+h', self.show_translation_history, suppress=False)
                
                # Auto-translate hotkey (Ctrl+C) - monitor clipboard changes
                keyboard.add_hotkey('ctrl+c', self.auto_translate_selection, suppress=False)
                
                self.hotkeys_enabled = True
                print("[SUCCESS] QTranslate hotkeys registered successfully!")
                
                # Show notification about available hotkeys
                try:
                    self.tray_icon.showMessage(
                        "快捷鍵已啟用", 
                        "QTranslate風格快捷鍵已啟用\nCtrl+C: 自動翻譯\nCtrl+Q: 彈出翻譯\nCtrl+Shift+T: 手動翻譯", 
                        QSystemTrayIcon.Information, 
                        3000
                    )
                except Exception as msg_error:
                    print(f"[WARNING] Failed to show hotkey notification: {msg_error}")
                
            except (OSError, PermissionError, Exception) as hotkey_error:
                print(f"[ERROR] Hotkey registration failed: {hotkey_error}")
                raise hotkey_error
                
        except Exception as e:
            print(f"[ERROR] Keyboard library error: {e}")
            print("[INFO] Running in SAFE MODE without hotkeys")
            self.hotkeys_enabled = False
            
            # Show safe mode notification
            try:
                self.tray_icon.showMessage(
                    "安全模式", 
                    "由於Windows權限限制，熱鍵已禁用。\n已啟用剪貼板監控功能：複製文字後會自動翻譯。\n也可使用系統托盤菜單訪問所有功能。", 
                    QSystemTrayIcon.Information, 
                    8000
                )
            except Exception as msg_error:
                print(f"[WARNING] Failed to show safe mode notification: {msg_error}")
            
            # Enhance system tray menu for safe mode
            try:
                self.enhance_tray_menu_for_safe_mode()
            except Exception as menu_error:
                print(f"[WARNING] Failed to enhance tray menu: {menu_error}")
            
            # Start clipboard monitor as alternative to hotkeys
            try:
                self.start_clipboard_monitor()
            except Exception as clipboard_error:
                print(f"[WARNING] Failed to start clipboard monitor: {clipboard_error}")
    
    def start_clipboard_monitor(self):
        """Start clipboard monitoring for auto-translation when hotkeys fail"""
        try:
            self.clipboard_timer = QTimer()
            self.clipboard_timer.timeout.connect(self.check_clipboard)
            self.last_clipboard_content = ""
            # Check clipboard every 2 seconds when in safe mode
            self.clipboard_timer.start(2000)
            print("[INFO] Started clipboard monitor as hotkey alternative")
        except Exception as e:
            print(f"[WARNING] Failed to start clipboard monitor: {e}")
    
    def check_clipboard(self):
        """Check clipboard for new content and auto-translate if configured"""
        try:
            if not self.config.get('translation', {}).get('auto_translate', True):
                return
                
            current_content = pyperclip.paste()
            if (current_content and 
                current_content != self.last_clipboard_content and
                current_content.strip()):
                
                text = current_content.strip()
                
                # Apply same filters as auto_translate_selection
                if (len(text) >= 2 and  
                    len(text) <= 500 and  
                    not text.isdigit() and  
                    not self.is_url(text) and  
                    not self.is_single_word_english(text)):
                    
                    self.last_clipboard_content = current_content
                    cursor_pos = QCursor.pos()
                    self.start_translation(text, cursor_pos)
                    print(f"[INFO] Clipboard auto-translate: {text[:30]}...")
                    
        except Exception as e:
            print(f"[WARNING] Clipboard monitor error: {e}")
    
    def enhance_tray_menu_for_safe_mode(self):
        """Add extra menu items when hotkeys are disabled"""
        try:
            tray_menu = self.tray_icon.contextMenu()
            
            # Add manual translate option at the top
            manual_action = QAction("🔄 手動翻譯", self.app)
            manual_action.triggered.connect(self.manual_translate)
            tray_menu.insertAction(tray_menu.actions()[0], manual_action)
            
            # Add auto translate option
            auto_action = QAction("⚡ 自動翻譯選取的文字", self.app)
            auto_action.triggered.connect(self.auto_translate_selection)
            tray_menu.insertAction(tray_menu.actions()[1], auto_action)
            
            # Add separator
            separator = QAction(self.app)
            separator.setSeparator(True)
            tray_menu.insertAction(tray_menu.actions()[2], separator)
            
            print("[INFO] Enhanced tray menu for safe mode")
            
        except Exception as e:
            print(f"[WARNING] Failed to enhance tray menu: {e}")
        
    def auto_translate_selection(self):
        """自動翻譯選取的文字 (Alt+C)"""
        try:
            # 檢查是否啟用自動翻譯
            if not self.config.get('translation', {}).get('auto_translate', True):
                self.tray_icon.showMessage(
                    "自動翻譯", 
                    "自動翻譯已禁用，請在設置中啟用。", 
                    QSystemTrayIcon.Warning, 
                    2000
                )
                return
            
            # 獲取剪貼板內容
            selected_text = pyperclip.paste()
            if selected_text and selected_text.strip():
                text = selected_text.strip()
                
                # 過濾條件
                if (len(text) >= 2 and  # 至少2個字符
                    len(text) <= 500 and  # 不超過500字符
                    not text.isdigit() and  # 不是純數字
                    not self.is_url(text) and  # 不是URL
                    not self.is_single_word_english(text)):  # 不是單個英文單詞
                    
                    # 獲取鼠標位置
                    cursor_pos = QCursor.pos()
                    self.start_translation(text, cursor_pos)
                    print(f"[INFO] Auto-translating: {text[:30]}...")
                else:
                    print(f"[INFO] Text filtered out: {text[:30]}...")
            else:
                self.tray_icon.showMessage(
                    "自動翻譯", 
                    "剪貼板沒有文本內容！", 
                    QSystemTrayIcon.Information, 
                    2000
                )
        except Exception as e:
            print(f"[ERROR] Error in auto-translate selection: {e}")
    
    def check_basic_hotkeys(self, event):
        """Deprecated - kept for compatibility"""
        pass
    
    def process_copied_text(self):
        """Deprecated - kept for compatibility"""
        pass
    
    def is_url(self, text):
        """檢查是否為URL"""
        return text.startswith(('http://', 'https://', 'www.', 'ftp://'))
    
    def is_single_word_english(self, text):
        """檢查是否為單個英文單詞（避免翻譯單詞）"""
        if len(text.split()) == 1 and text.isalpha() and all(ord(c) < 128 for c in text):
            return len(text) < 15  # 短於15個字符的單個英文單詞
        return False
    
    def handle_copied_text(self, text):
        """在主線程中處理複製的文字"""
        try:
            print(f"[INFO] Processing text: {text[:50]}...")  # 調試信息
            # 獲取滑鼠位置（在主線程中安全調用）
            cursor_pos = QCursor.pos()
            print(f"[INFO] Mouse position: {cursor_pos.x()}, {cursor_pos.y()}")  # 調試信息
            # 開始翻譯
            self.start_translation(text, cursor_pos)
        except Exception as e:
            print(f"[ERROR] Error handling copied text: {e}")
            import traceback
            traceback.print_exc()
    
    def start_translation(self, text, pos):
        """開始翻譯工作"""
        try:
            print(f"[INFO] Starting translation for: {text[:30]}...")  # 調試信息
            
            # 顯示翻譯視窗
            self.translator_window.show_at_position(pos)
            self.translator_window.result_label.setText("翻譯中...")
            
            print("[SUCCESS] Translation window shown")  # 調試信息
            
            # 停止之前的翻譯工作（如果有的話）
            if self.translation_worker and self.translation_worker.isRunning():
                self.translation_worker.quit()
                self.translation_worker.wait()
            
            # 啟動翻譯工作線程（集成翻譯記憶庫）
            self.translation_worker = TranslationWorker(
                text, self.config, self.translation_memory, 'auto', 
                self.config.get('translation', {}).get('default_target', 'zh-TW')
            )
            
            # Store text for signal handler
            self.current_translation_text = text
            
            # 連接信號 - 使用直接方法確保信號正常工作
            self.translation_worker.translation_complete.connect(self.on_translation_complete)
            self.translation_worker.translation_error.connect(self.on_translation_error)
            
            print(f"[DEBUG] Signal connections established")
            
            print("[INFO] Starting translation worker...")  # 調試信息
            
            self.translation_worker.start()
            
        except Exception as e:
            print(f"[ERROR] Error starting translation: {e}")
            import traceback
            traceback.print_exc()
            # 顯示錯誤到翻譯窗口
            try:
                self.translator_window.show_at_position(pos)
                self.translator_window.show_error(f"翻譯啟動失敗: {str(e)}")
            except:
                print("[ERROR] Failed to show error window")
    
    def handle_translation_result(self, original_text, translation):
        """處理翻譯結果並顯示到UI"""
        print(f"[DEBUG] *** SIGNAL RECEIVED *** handle_translation_result called!")
        print(f"[DEBUG] Original text: {original_text[:30] if original_text else 'None'}...")
        print(f"[DEBUG] Translation: {translation[:50] if translation else 'None'}...")
        
        try:
            if translation and translation.strip():
                print(f"[DEBUG] Calling show_translation with valid result...")
                self.translator_window.show_translation(original_text, translation)
                print(f"[SUCCESS] Translation displayed: {translation[:50]}...")
            else:
                print("[ERROR] Empty translation result")
                self.translator_window.show_error("翻譯結果為空")
                
        except Exception as e:
            print(f"[ERROR] Error handling translation result: {e}")
            import traceback
            traceback.print_exc()
            self.translator_window.show_error(f"顯示翻譯結果時出錯: {str(e)}")
    
    def on_translation_complete(self, result):
        """處理翻譯完成信號"""
        print(f"[DEBUG] *** TRANSLATION COMPLETE SIGNAL *** Result: {result[:50] if result else 'None'}...")
        try:
            original_text = getattr(self, 'current_translation_text', 'Unknown')
            self.handle_translation_result(original_text, result)
        except Exception as e:
            print(f"[ERROR] Error in on_translation_complete: {e}")
            import traceback
            traceback.print_exc()
    
    def on_translation_error(self, error):
        """處理翻譯錯誤信號"""
        print(f"[DEBUG] *** TRANSLATION ERROR SIGNAL *** Error: {error}")
        try:
            self.translator_window.show_error(str(error))
        except Exception as e:
            print(f"[ERROR] Error in on_translation_error: {e}")
    
    def test_signal_handler(self, result):
        """測試信號處理器"""
        print(f"[DEBUG] *** TEST SIGNAL HANDLER CALLED *** Result: {result[:50] if result else 'None'}...")
    
    def test_translation(self):
        """測試翻譯功能"""
        print("[INFO] Starting test translation...")
        
        # 直接測試顯示功能
        try:
            cursor_pos = QCursor.pos()
            self.translator_window.show_at_position(cursor_pos)
            self.translator_window.show_translation("Hello", "你好")
            print("[SUCCESS] Direct translation display test completed")
        except Exception as e:
            print(f"[ERROR] Direct display test failed: {e}")
        
        # 測試翻譯工作線程
        try:
            test_text = "Hello world"
            self.start_translation(test_text, QCursor.pos())
            print("[SUCCESS] Translation worker test started")
        except Exception as e:
            print(f"[ERROR] Translation worker test failed: {e}")
    
    def apply_theme(self):
        """Apply current theme to UI components"""
        try:
            # Apply theme to main popup window
            window_style = self.theme_manager.get_stylesheet("Window")
            button_style = self.theme_manager.get_stylesheet("Button")
            edit_style = self.theme_manager.get_stylesheet("Edit")
            
            combined_style = f"{window_style}\n{button_style}\n{edit_style}"
            self.translator_window.setStyleSheet(combined_style)
        except Exception as e:
            print(f"Theme application error: {e}")
    
    def select_service(self, service_index: int):
        """Select translation service by index (QTranslate hotkey feature)"""
        if 0 <= service_index < len(self.service_order):
            service_name = self.service_order[service_index]
            self.multi_service_translator.active_service = service_name
            
            # Update config and show notification
            if 'translation_service' not in self.config:
                self.config['translation_service'] = {}
            self.config['translation_service']['provider'] = service_name
            self.save_config()
            
            service_info = self.multi_service_translator.get_service_info(service_name)
            service_display_name = service_info.get('name', service_name.title())
            
            self.tray_icon.showMessage(
                "翻譯服務切換", 
                f"已切換到: {service_display_name}", 
                QSystemTrayIcon.Information, 
                2000
            )
    
    def select_language(self, language_index: int):
        """Select target language by index (QTranslate hotkey feature)"""
        languages = self.translation_memory.get_enabled_languages()
        if 0 <= language_index < len(languages):
            lang_code, lang_name, native_name = languages[language_index]
            
            # Update config
            if 'translation' not in self.config:
                self.config['translation'] = {}
            self.config['translation']['default_target'] = lang_code
            self.save_config()
            
            self.tray_icon.showMessage(
                "目標語言切換", 
                f"已切換到: {native_name} ({lang_name})", 
                QSystemTrayIcon.Information, 
                2000
            )
    
    def switch_languages(self):
        """Switch source and target languages (QTranslate Ctrl+I feature)"""
        try:
            current_source = self.config.get('translation', {}).get('default_source', 'auto')
            current_target = self.config.get('translation', {}).get('default_target', 'zh-TW')
            
            # Only switch if source is not auto-detect
            if current_source != 'auto':
                if 'translation' not in self.config:
                    self.config['translation'] = {}
                self.config['translation']['default_source'] = current_target
                self.config['translation']['default_target'] = current_source
                self.save_config()
                
                self.tray_icon.showMessage(
                    "語言切換", 
                    f"源語言和目標語言已交換", 
                    QSystemTrayIcon.Information, 
                    2000
                )
            else:
                self.tray_icon.showMessage(
                    "語言切換", 
                    "無法切換：源語言為自動檢測", 
                    QSystemTrayIcon.Warning, 
                    2000
                )
        except Exception as e:
            print(f"Language switch error: {e}")
    
    def show_popup_translation(self):
        """Show popup translation for clipboard content (QTranslate Ctrl+Q)"""
        try:
            text = pyperclip.paste().strip()
            if text:
                cursor_pos = QCursor.pos()
                self.start_translation(text, cursor_pos)
            else:
                self.tray_icon.showMessage(
                    "彈出翻譯", 
                    "剪貼板沒有文本內容！", 
                    QSystemTrayIcon.Warning, 
                    2000
                )
        except Exception as e:
            print(f"Popup translation error: {e}")
    
    def web_search_selection(self):
        """Search selected text on web (QTranslate Ctrl+Shift+Q)"""
        try:
            text = pyperclip.paste().strip()
            if text:
                # Use Google search by default
                search_url = f"https://www.google.com/search?q={quote(text)}"
                from PyQt5.QtGui import QDesktopServices
                from PyQt5.QtCore import QUrl
                QDesktopServices.openUrl(QUrl(search_url))
            else:
                self.tray_icon.showMessage(
                    "網路搜尋", 
                    "剪貼板沒有文本內容！", 
                    QSystemTrayIcon.Warning, 
                    2000
                )
        except Exception as e:
            print(f"Web search error: {e}")
    
    def listen_selected_text(self):
        """Listen to selected text using TTS (QTranslate Ctrl+E)"""
        try:
            text = pyperclip.paste().strip()
            if text:
                # Detect language for proper TTS
                detector = LanguageDetector()
                detected_lang = detector.detect_language(text)
                
                # Use speech manager to speak text
                self.speech_manager.speak_text(text, detected_lang)
                
                self.tray_icon.showMessage(
                    "語音播放", 
                    f"正在播放: {text[:50]}{'...' if len(text) > 50 else ''}", 
                    QSystemTrayIcon.Information, 
                    2000
                )
            else:
                self.tray_icon.showMessage(
                    "語音播放", 
                    "剪貼板沒有文本內容！", 
                    QSystemTrayIcon.Warning, 
                    2000
                )
        except Exception as e:
            print(f"TTS error: {e}")
    
    def show_dictionary(self):
        """Show dictionary window for selected text (QTranslate Ctrl+D)"""
        try:
            text = pyperclip.paste().strip()
            if text:
                # Get first word for dictionary lookup
                word = text.split()[0] if text.split() else text
                
                # Open dictionary URL
                dict_url = self.dictionary_manager.lookup_word(word, "oxford")
                if dict_url:
                    from PyQt5.QtGui import QDesktopServices
                    from PyQt5.QtCore import QUrl
                    QDesktopServices.openUrl(QUrl(dict_url))
                else:
                    self.tray_icon.showMessage(
                        "字典查詢", 
                        "無法查詢該詞語", 
                        QSystemTrayIcon.Warning, 
                        2000
                    )
            else:
                self.tray_icon.showMessage(
                    "字典查詢", 
                    "剪貼板沒有文本內容！", 
                    QSystemTrayIcon.Warning, 
                    2000
                )
        except Exception as e:
            print(f"Dictionary lookup error: {e}")
    
    def start_ocr_translation(self):
        """Start OCR-based translation (QTranslate-inspired)"""
        try:
            self.tray_icon.showMessage(
                "OCR翻譯", 
                "請選擇要翻譯的螢幕區域...", 
                QSystemTrayIcon.Information, 
                2000
            )
            
            # Start screen capture for OCR
            def ocr_callback(extracted_text):
                if extracted_text:
                    cursor_pos = QCursor.pos()
                    self.start_translation(extracted_text, cursor_pos)
            
            self.ocr_translator.start_screen_capture(ocr_callback)
            
        except Exception as e:
            print(f"OCR translation error: {e}")
    
    def start_speech_input(self):
        """Start speech-to-text input (QTranslate-inspired)"""
        try:
            self.tray_icon.showMessage(
                "語音輸入", 
                "開始語音識別...", 
                QSystemTrayIcon.Information, 
                2000
            )
            
            def stt_callback(recognized_text):
                if recognized_text:
                    cursor_pos = QCursor.pos()
                    self.start_translation(recognized_text, cursor_pos)
            
            self.speech_manager.start_speech_recognition(stt_callback)
            
        except Exception as e:
            print(f"Speech input error: {e}")
    
    def toggle_mouse_mode(self):
        """Toggle mouse mode (QTranslate tray click feature)"""
        mode_names = {
            QTranslateAdvancedFeatures.MOUSE_MODE_DISABLED: "禁用",
            QTranslateAdvancedFeatures.MOUSE_MODE_ICON_SHOW: "顯示圖標",
            QTranslateAdvancedFeatures.MOUSE_MODE_INSTANT_TRANSLATE: "即時翻譯",
            QTranslateAdvancedFeatures.MOUSE_MODE_INSTANT_TRANSLATE_AND_LISTEN: "即時翻譯+語音"
        }
        
        # Cycle through modes
        current_mode = self.mouse_mode
        next_mode = (current_mode + 1) % 4
        self.mouse_mode = next_mode
        
        mode_name = mode_names.get(next_mode, "未知")
        self.tray_icon.showMessage(
            "滑鼠模式", 
            f"已切換到: {mode_name}", 
            QSystemTrayIcon.Information, 
            2000
        )
    
    def set_theme(self, theme_name: str):
        """Set application theme"""
        try:
            self.theme_manager.set_theme(theme_name)
            self.apply_theme()
            
            # Update config
            if 'ui' not in self.config:
                self.config['ui'] = {}
            self.config['ui']['theme'] = theme_name
            self.save_config()
            
            self.tray_icon.showMessage(
                "主題切換", 
                f"已切換到: {theme_name}", 
                QSystemTrayIcon.Information, 
                2000
            )
        except Exception as e:
            print(f"Theme setting error: {e}")
                
    def run(self):
        """運行應用程序"""
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    # 創建並運行翻譯應用
    translator_app = TranslatorApp()
    translator_app.run() 