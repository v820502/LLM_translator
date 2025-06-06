#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM翻譯器完整測試套件
包含Unit Tests和Integration Tests
"""

import unittest
import sys
import os
import json
import sqlite3
import time
import threading
import tempfile
from unittest.mock import Mock, patch, MagicMock
import pyperclip

# 添加當前目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 導入要測試的模組
try:
    from translator import (
        TranslationMemory, LanguageDetector, TranslationWorker,
        TranslatorApp, TranslatorWindow, ThemeManager, 
        QTranslateAdvancedFeatures, MultiServiceTranslator
    )
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QThread, pyqtSignal
    from PyQt5.QtTest import QTest
    IMPORTS_AVAILABLE = True
except ImportError as e:
    print(f"警告: 無法導入部分模組: {e}")
    IMPORTS_AVAILABLE = False

class TestTranslationMemory(unittest.TestCase):
    """翻譯記憶庫測試"""
    
    def setUp(self):
        """設置測試環境"""
        if not IMPORTS_AVAILABLE:
            self.skipTest("Required imports not available")
        
        # 使用臨時資料庫
        self.test_db = tempfile.mktemp(suffix='.db')
        self.memory = TranslationMemory(self.test_db)
    
    def tearDown(self):
        """清理測試環境"""
        if hasattr(self, 'test_db') and os.path.exists(self.test_db):
            try:
                os.remove(self.test_db)
            except Exception:
                pass
    
    def test_database_initialization(self):
        """測試資料庫初始化"""
        self.assertTrue(os.path.exists(self.test_db))
        
        # 檢查表結構
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        self.assertIn('translations', tables)
        self.assertIn('multilingual_content', tables)
        self.assertIn('language_config', tables)
    
    def test_save_and_get_translation(self):
        """測試保存和獲取翻譯"""
        source_text = "Hello world"
        target_text = "你好世界"
        source_lang = "en"
        target_lang = "zh-TW"
        provider = "google"
        
        # 保存翻譯
        self.memory.save_translation(source_text, target_text, source_lang, target_lang, provider)
        
        # 獲取翻譯
        result = self.memory.get_translation(source_text, source_lang, target_lang)
        self.assertEqual(result, target_text)
    
    def test_multilingual_content(self):
        """測試多語言內容管理"""
        content_id = "test_content"
        language = "zh-TW"
        content = "測試內容"
        title = "測試標題"
        
        self.memory.save_multilingual_content(content_id, language, content, title)
        
        # 驗證數據已保存
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM multilingual_content WHERE content_id = ? AND language = ?",
            (content_id, language)
        )
        result = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(result)
        self.assertEqual(result[2], content)  # content欄位
        self.assertEqual(result[3], title)    # title欄位

class TestLanguageDetector(unittest.TestCase):
    """語言檢測測試"""
    
    def setUp(self):
        if not IMPORTS_AVAILABLE:
            self.skipTest("Required imports not available")
        self.detector = LanguageDetector()
    
    def test_english_detection(self):
        """測試英文檢測"""
        text = "Hello, how are you today?"
        result = self.detector.detect_language(text)
        # 應該檢測為英文或auto
        self.assertIn(result, ['en', 'auto'])
    
    def test_chinese_detection(self):
        """測試中文檢測"""
        text = "你好，今天天氣如何？"
        result = self.detector.detect_language(text)
        # 應該檢測為中文相關
        self.assertIn(result, ['zh', 'zh-CN', 'zh-TW', 'auto'])
    
    def test_empty_text(self):
        """測試空文本"""
        result = self.detector.detect_language("")
        self.assertEqual(result, 'en')  # 默認返回英文

class TestThemeManager(unittest.TestCase):
    """主題管理器測試"""
    
    def setUp(self):
        if not IMPORTS_AVAILABLE:
            self.skipTest("Required imports not available")
        self.theme_manager = ThemeManager()
    
    def test_available_themes(self):
        """測試可用主題"""
        themes = self.theme_manager.themes
        self.assertIn("Photoshop Dark", themes)
        self.assertIn("Holo Light", themes)
        self.assertIn("Metro", themes)
    
    def test_set_theme(self):
        """測試設置主題"""
        theme_name = "Holo Light"
        self.theme_manager.set_theme(theme_name)
        self.assertEqual(self.theme_manager.current_theme, theme_name)
    
    def test_get_stylesheet(self):
        """測試獲取樣式表"""
        stylesheet = self.theme_manager.get_stylesheet("Button")
        self.assertIsInstance(stylesheet, str)
        self.assertGreater(len(stylesheet), 0)

class TestMultiServiceTranslator(unittest.TestCase):
    """多服務翻譯器測試"""
    
    def setUp(self):
        if not IMPORTS_AVAILABLE:
            self.skipTest("Required imports not available")
        self.translator = MultiServiceTranslator()
    
    def test_service_info(self):
        """測試服務信息"""
        google_info = self.translator.get_service_info("google")
        self.assertIn("name", google_info)
        self.assertIn("capabilities", google_info)
        self.assertIn("languages", google_info)
    
    def test_capabilities(self):
        """測試服務能力"""
        # Google應該支持翻譯功能
        supports_translate = self.translator.supports_capability(
            "google", QTranslateAdvancedFeatures.CAPABILITY_TRANSLATE
        )
        self.assertTrue(supports_translate)
    
    def test_supported_languages(self):
        """測試支持的語言"""
        languages = self.translator.get_supported_languages("google")
        self.assertIn("en", languages)
        self.assertIn("zh-cn", languages)
        self.assertGreater(len(languages), 10)

class TestConfigurationLoad(unittest.TestCase):
    """配置文件載入測試"""
    
    def test_config_file_exists(self):
        """測試配置文件存在"""
        self.assertTrue(os.path.exists("config.json"))
    
    def test_config_file_valid_json(self):
        """測試配置文件是有效的JSON"""
        with open("config.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 檢查必要的配置項
        self.assertIn("auto_translate", config)
        self.assertIn("source_language", config)
        self.assertIn("target_language", config)
        self.assertIn("translation_service", config)
    
    def test_config_structure(self):
        """測試配置文件結構"""
        with open("config.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 檢查主要部分
        expected_sections = [
            "translation_service", "hotkeys", "ui", "speech", 
            "ocr", "dictionary", "advanced", "translation"
        ]
        
        for section in expected_sections:
            self.assertIn(section, config, f"Missing config section: {section}")

class TestIntegrationClipboard(unittest.TestCase):
    """剪貼簿整合測試"""
    
    def test_clipboard_functionality(self):
        """測試剪貼簿基本功能"""
        test_text = "Integration test text"
        
        # 設置剪貼簿
        pyperclip.copy(test_text)
        time.sleep(0.1)  # 等待設置完成
        
        # 讀取剪貼簿
        result = pyperclip.paste()
        self.assertEqual(result, test_text)

class TestApplicationIntegration(unittest.TestCase):
    """應用程式整合測試"""
    
    def setUp(self):
        if not IMPORTS_AVAILABLE:
            self.skipTest("Required imports not available")
        
        # 創建QApplication如果不存在
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
    
    def test_translator_app_creation(self):
        """測試翻譯器應用程式創建"""
        try:
            translator_app = TranslatorApp()
            self.assertIsNotNone(translator_app)
            self.assertTrue(hasattr(translator_app, 'config'))
            self.assertTrue(hasattr(translator_app, 'translation_memory'))
        except Exception as e:
            self.fail(f"Failed to create TranslatorApp: {e}")
    
    def test_translator_window_creation(self):
        """測試翻譯窗口創建"""
        try:
            window = TranslatorWindow()
            self.assertIsNotNone(window)
            self.assertTrue(hasattr(window, 'result_label'))
            self.assertTrue(hasattr(window, 'copy_button'))
        except Exception as e:
            self.fail(f"Failed to create TranslatorWindow: {e}")

class TestBuildVerification(unittest.TestCase):
    """Build驗證測試"""
    
    def test_executable_exists(self):
        """測試可執行文件存在"""
        exe_path = os.path.join("dist", "LLM_Translator.exe")
        if os.path.exists(exe_path):
            self.assertTrue(os.path.isfile(exe_path))
            # 檢查文件大小（應該大於10MB）
            file_size = os.path.getsize(exe_path)
            self.assertGreater(file_size, 10 * 1024 * 1024)  # 10MB
        else:
            self.skipTest("Executable not found - build may not have completed")
    
    def test_required_files_exist(self):
        """測試必要文件存在"""
        required_files = [
            "translator.py",
            "config.json", 
            "requirements.txt",
            "build_windows.bat",
            "icon.png"
        ]
        
        for filename in required_files:
            self.assertTrue(os.path.exists(filename), f"Missing required file: {filename}")

class TestPerformance(unittest.TestCase):
    """性能測試"""
    
    def test_translation_memory_performance(self):
        """測試翻譯記憶庫性能"""
        if not IMPORTS_AVAILABLE:
            self.skipTest("Required imports not available")
        
        test_db = tempfile.mktemp(suffix='.db')
        memory = TranslationMemory(test_db)
        
        try:
            # 批量插入測試
            start_time = time.time()
            for i in range(100):
                memory.save_translation(
                    f"Test text {i}", 
                    f"測試文字 {i}", 
                    "en", 
                    "zh-TW", 
                    "test"
                )
            insert_time = time.time() - start_time
            
            # 批量查詢測試
            start_time = time.time()
            for i in range(100):
                result = memory.get_translation(f"Test text {i}", "en", "zh-TW")
                self.assertIsNotNone(result)
            query_time = time.time() - start_time
            
            # 性能應該合理
            self.assertLess(insert_time, 5.0, "Translation memory insert too slow")
            self.assertLess(query_time, 2.0, "Translation memory query too slow")
            
        finally:
            if os.path.exists(test_db):
                os.remove(test_db)

def run_test_suite():
    """執行完整測試套件"""
    print("開始執行LLM翻譯器測試套件")
    print("=" * 60)
    
    # 創建測試套件
    test_classes = [
        TestTranslationMemory,
        TestLanguageDetector, 
        TestThemeManager,
        TestMultiServiceTranslator,
        TestConfigurationLoad,
        TestIntegrationClipboard,
        TestApplicationIntegration,
        TestBuildVerification,
        TestPerformance
    ]
    
    overall_result = True
    results = {}
    
    for test_class in test_classes:
        print(f"\n執行 {test_class.__name__}...")
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        runner = unittest.TextTestRunner(verbosity=1, stream=sys.stdout)
        result = runner.run(suite)
        
        success = result.wasSuccessful()
        results[test_class.__name__] = {
            'success': success,
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors)
        }
        
        if not success:
            overall_result = False
            print(f"❌ {test_class.__name__} 失敗")
            for failure in result.failures:
                print(f"   失敗: {failure[0]}")
            for error in result.errors:
                print(f"   錯誤: {error[0]}")
        else:
            print(f"✅ {test_class.__name__} 通過")
    
    # 總結報告
    print("\n" + "=" * 60)
    print("測試結果總結:")
    
    total_tests = 0
    total_failures = 0
    total_errors = 0
    
    for test_name, result in results.items():
        status = "✅ 通過" if result['success'] else "❌ 失敗"
        print(f"   {test_name}: {status} ({result['tests_run']} 測試)")
        
        total_tests += result['tests_run']
        total_failures += result['failures']
        total_errors += result['errors']
    
    print(f"\n總計: {total_tests} 測試")
    print(f"失敗: {total_failures}")
    print(f"錯誤: {total_errors}")
    
    if overall_result:
        print("\n所有測試通過！")
        return 0
    else:
        print("\n部分測試失敗！")
        return 1

if __name__ == "__main__":
    exit_code = run_test_suite()
    sys.exit(exit_code) 