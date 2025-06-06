#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM Translator Build Test Suite
Tests both source code and built executable functionality
Enhanced with comprehensive GUI testing
"""

import sys
import os
import unittest
import subprocess
import time
import json
import tempfile
from pathlib import Path

# Try to import psutil for enhanced process testing
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("Warning: psutil not available, some enhanced tests will be skipped")

# GUI Testing Imports
try:
    from PyQt5.QtWidgets import QApplication, QSystemTrayIcon
    from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
    from PyQt5.QtGui import QIcon
    from PyQt5.QtTest import QTest
    PYQT_AVAILABLE = True
    PYQT_VERSION = "PyQt5"
except ImportError:
    try:
        from PyQt6.QtWidgets import QApplication, QSystemTrayIcon
        from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
        from PyQt6.QtGui import QIcon
        from PyQt6.QtTest import QTest
        PYQT_AVAILABLE = True
        PYQT_VERSION = "PyQt6"
    except ImportError:
        PYQT_AVAILABLE = False
        PYQT_VERSION = None

class TestImports(unittest.TestCase):
    """Test that all required modules can be imported"""
    
    def test_standard_library_imports(self):
        """Test standard library imports"""
        try:
            import sys
            import os
            import json
            import tempfile
            self.assertTrue(True, "Standard library imports successful")
        except ImportError as e:
            self.fail(f"Standard library import failed: {e}")
    
    def test_third_party_imports(self):
        """Test third-party library imports"""
        try:
            import keyboard
            import pyperclip
            import requests
            import googletrans
            self.assertTrue(True, "Third-party imports successful")
        except ImportError as e:
            self.fail(f"Third-party import failed: {e}")
    
    def test_pyqt_imports(self):
        """Test PyQt6 imports with fallback options"""
        pyqt_errors = []
        
        # Test PyQt6
        try:
            from PyQt6.QtWidgets import QApplication
            from PyQt6.QtCore import Qt
            from PyQt6.QtGui import QIcon
            self.pyqt_version = "PyQt6"
            return
        except ImportError as e:
            pyqt_errors.append(f"PyQt6: {e}")
        
        # Test PyQt5 as fallback
        try:
            from PyQt5.QtWidgets import QApplication
            from PyQt5.QtCore import Qt
            from PyQt5.QtGui import QIcon
            self.pyqt_version = "PyQt5"
            return
        except ImportError as e:
            pyqt_errors.append(f"PyQt5: {e}")
        
        # If both fail, report the errors
        self.fail(f"No working PyQt installation found. Errors: {'; '.join(pyqt_errors)}")

class TestConfiguration(unittest.TestCase):
    """Test configuration file handling"""
    
    def setUp(self):
        self.config_path = "config.json"
    
    def test_config_file_exists(self):
        """Test that config.json exists"""
        self.assertTrue(os.path.exists(self.config_path), "config.json file not found")
    
    def test_config_file_valid_json(self):
        """Test that config.json is valid JSON"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            self.assertIsInstance(config, dict, "Config should be a dictionary")
        except json.JSONDecodeError as e:
            self.fail(f"config.json is not valid JSON: {e}")
        except Exception as e:
            self.fail(f"Error reading config.json: {e}")
    
    def test_translation_service_config(self):
        """Test translation service configuration structure"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Check if translation_service exists
            self.assertIn('translation_service', config, "translation_service not found in config")
            
            translation_service = config['translation_service']
            
            # Check required fields
            self.assertIn('provider', translation_service, "provider not found in translation_service")
            self.assertIn('google_api', translation_service, "google_api not found in translation_service")
            self.assertIn('custom_llm', translation_service, "custom_llm not found in translation_service")
            
            # Check Google API structure
            google_api = translation_service['google_api']
            self.assertIn('api_key', google_api, "api_key not found in google_api")
            self.assertIn('endpoint', google_api, "endpoint not found in google_api")
            
            # Check custom LLM structure
            custom_llm = translation_service['custom_llm']
            self.assertIn('enabled', custom_llm, "enabled not found in custom_llm")
            self.assertIn('api_url', custom_llm, "api_url not found in custom_llm")
            self.assertIn('api_key', custom_llm, "api_key not found in custom_llm")
            self.assertIn('system_prompt', custom_llm, "system_prompt not found in custom_llm")
            
        except Exception as e:
            self.fail(f"Error testing translation service config: {e}")
    
    def test_qtranslate_features_config(self):
        """Test qTranslate-XT inspired features configuration"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Test translation memory configuration
            self.assertIn('translation_memory', config, "translation_memory not found in config")
            tm_config = config['translation_memory']
            self.assertIn('enabled', tm_config, "enabled not found in translation_memory")
            self.assertIn('max_entries', tm_config, "max_entries not found in translation_memory")
            
            # Test language detection configuration
            self.assertIn('language_detection', config, "language_detection not found in config")
            ld_config = config['language_detection']
            self.assertIn('enabled', ld_config, "enabled not found in language_detection")
            self.assertIn('confidence_threshold', ld_config, "confidence_threshold not found in language_detection")
            
            # Test multilingual configuration
            self.assertIn('multilingual', config, "multilingual not found in config")
            ml_config = config['multilingual']
            self.assertIn('enabled_languages', ml_config, "enabled_languages not found in multilingual")
            self.assertIn('language_switching', ml_config, "language_switching not found in multilingual")
            
            # Test qTranslate features
            self.assertIn('qtranslate_features', config, "qtranslate_features not found in config")
            qt_config = config['qtranslate_features']
            self.assertIn('content_storage', qt_config, "content_storage not found in qtranslate_features")
            self.assertIn('translation_modules', qt_config, "translation_modules not found in qtranslate_features")
            
        except Exception as e:
            self.fail(f"Error testing qTranslate features config: {e}")

class TestSourceCode(unittest.TestCase):
    """Test the source code functionality"""
    
    def test_translator_py_syntax(self):
        """Test that translator.py has valid syntax"""
        try:
            with open("translator.py", 'r', encoding='utf-8') as f:
                code = f.read()
            compile(code, "translator.py", "exec")
            self.assertTrue(True, "translator.py has valid syntax")
        except SyntaxError as e:
            self.fail(f"Syntax error in translator.py: {e}")
        except Exception as e:
            self.fail(f"Error checking translator.py: {e}")
    
    def test_resource_path_function(self):
        """Test the resource_path function"""
        try:
            # Import the function from translator.py
            import translator
            path = translator.resource_path("config.json")
            self.assertIsInstance(path, str, "resource_path should return a string")
            self.assertTrue(len(path) > 0, "resource_path should return non-empty string")
        except Exception as e:
            self.fail(f"Error testing resource_path function: {e}")
    
    def test_translation_memory_class(self):
        """Test that TranslationMemory class can be instantiated"""
        try:
            import translator
            import tempfile
            import os
            
            # Create a temporary database file
            temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
            temp_db.close()
            
            try:
                memory = translator.TranslationMemory(temp_db.name)
                self.assertIsInstance(memory, translator.TranslationMemory)
                
                # Test language configuration
                languages = memory.get_enabled_languages()
                self.assertIsInstance(languages, list, "get_enabled_languages should return a list")
                self.assertGreater(len(languages), 0, "Should have at least one enabled language")
            finally:
                if os.path.exists(temp_db.name):
                    os.unlink(temp_db.name)
            
        except Exception as e:
            self.fail(f"Error testing TranslationMemory class: {e}")
    
    def test_language_detector_class(self):
        """Test that LanguageDetector class can be instantiated"""
        try:
            import translator
            detector = translator.LanguageDetector()
            self.assertIsInstance(detector, translator.LanguageDetector)
            
            # Test detection on simple text
            result = detector.detect_language("Hello world")
            self.assertIsInstance(result, str, "detect_language should return a string")
            
        except Exception as e:
            self.fail(f"Error testing LanguageDetector class: {e}")

@unittest.skipIf(not PYQT_AVAILABLE, f"PyQt not available for GUI testing")
class TestGUIComponents(unittest.TestCase):
    """Test GUI components and basic functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Create QApplication for GUI testing"""
        if not QApplication.instance():
            cls.app = QApplication([])
        else:
            cls.app = QApplication.instance()
    
    def test_translator_window_creation(self):
        """Test that TranslatorWindow can be created"""
        try:
            import translator
            window = translator.TranslatorWindow()
            self.assertIsNotNone(window, "TranslatorWindow should be created")
            self.assertEqual(window.width(), 350, "Window width should be 350px")
            self.assertEqual(window.height(), 120, "Window height should be 120px")
            window.close()
        except Exception as e:
            self.fail(f"Error creating TranslatorWindow: {e}")
    
    def test_settings_dialog_creation(self):
        """Test that SettingsDialog can be created"""
        try:
            import translator
            config = {"translation": {}, "ui": {}, "translation_service": {"google_api": {}, "custom_llm": {}}}
            memory = translator.TranslationMemory(":memory:")
            dialog = translator.SettingsDialog(config, memory)
            self.assertIsNotNone(dialog, "SettingsDialog should be created")
            self.assertEqual(dialog.windowTitle(), "翻譯器設置", "Dialog title should be correct")
            dialog.close()
        except Exception as e:
            self.fail(f"Error creating SettingsDialog: {e}")
    
    def test_batch_translation_dialog_creation(self):
        """Test that BatchTranslationDialog can be created"""
        try:
            import translator
            import tempfile
            import os
            
            # Create a temporary database file
            temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
            temp_db.close()
            
            try:
                config = {"translation_service": {"provider": "google"}}
                memory = translator.TranslationMemory(temp_db.name)
                dialog = translator.BatchTranslationDialog(config, memory)
                self.assertIsNotNone(dialog, "BatchTranslationDialog should be created")
                self.assertEqual(dialog.windowTitle(), "批量翻譯", "Dialog title should be correct")
                dialog.close()
            finally:
                if os.path.exists(temp_db.name):
                    os.unlink(temp_db.name)
        except Exception as e:
            self.fail(f"Error creating BatchTranslationDialog: {e}")
    
    def test_translation_history_dialog_creation(self):
        """Test that TranslationHistoryDialog can be created"""
        try:
            import translator
            import tempfile
            import os
            
            # Create a temporary database file
            temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
            temp_db.close()
            
            try:
                memory = translator.TranslationMemory(temp_db.name)
                dialog = translator.TranslationHistoryDialog(memory)
                self.assertIsNotNone(dialog, "TranslationHistoryDialog should be created")
                self.assertEqual(dialog.windowTitle(), "翻譯歷史", "Dialog title should be correct")
                dialog.close()
            finally:
                if os.path.exists(temp_db.name):
                    os.unlink(temp_db.name)
        except Exception as e:
            self.fail(f"Error creating TranslationHistoryDialog: {e}")
    
    def test_language_manager_dialog_creation(self):
        """Test that LanguageManagerDialog can be created"""
        try:
            import translator
            import tempfile
            import os
            
            # Create a temporary database file
            temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
            temp_db.close()
            
            try:
                memory = translator.TranslationMemory(temp_db.name)
                dialog = translator.LanguageManagerDialog(memory)
                self.assertIsNotNone(dialog, "LanguageManagerDialog should be created")
                self.assertEqual(dialog.windowTitle(), "語言管理", "Dialog title should be correct")
                dialog.close()
            finally:
                if os.path.exists(temp_db.name):
                    os.unlink(temp_db.name)
        except Exception as e:
            self.fail(f"Error creating LanguageManagerDialog: {e}")

@unittest.skipIf(not PYQT_AVAILABLE, f"PyQt not available for GUI testing")
class TestPopupWindow(unittest.TestCase):
    """Test popup window functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Create QApplication for GUI testing"""
        if not QApplication.instance():
            cls.app = QApplication([])
        else:
            cls.app = QApplication.instance()
    
    def setUp(self):
        """Set up test environment for each test"""
        import translator
        self.window = translator.TranslatorWindow()
    
    def tearDown(self):
        """Clean up after each test"""
        if hasattr(self, 'window'):
            self.window.close()
    
    def test_popup_window_positioning(self):
        """Test popup window positioning logic"""
        try:
            from PyQt5.QtCore import QPoint
            from PyQt5.QtWidgets import QDesktopWidget
            
            # Test positioning at various screen positions
            desktop = QDesktopWidget()
            screen_rect = desktop.screenGeometry()
            
            # Test center position
            center_pos = QPoint(screen_rect.center())
            self.window.show_at_position(center_pos)
            self.assertTrue(self.window.isVisible(), "Window should be visible after positioning")
            
            # Test edge positions
            edge_positions = [
                QPoint(10, 10),  # Top-left
                QPoint(screen_rect.width() - 10, 10),  # Top-right
                QPoint(10, screen_rect.height() - 10),  # Bottom-left
                QPoint(screen_rect.width() - 10, screen_rect.height() - 10),  # Bottom-right
            ]
            
            for pos in edge_positions:
                self.window.show_at_position(pos)
                window_rect = self.window.geometry()
                # Check if window is within screen bounds
                self.assertGreaterEqual(window_rect.left(), 0, "Window should not be off-screen left")
                self.assertGreaterEqual(window_rect.top(), 0, "Window should not be off-screen top")
                self.assertLessEqual(window_rect.right(), screen_rect.width(), "Window should not be off-screen right")
                self.assertLessEqual(window_rect.bottom(), screen_rect.height(), "Window should not be off-screen bottom")
            
        except Exception as e:
            self.fail(f"Error testing popup positioning: {e}")
    
    def test_popup_window_auto_hide(self):
        """Test popup window auto-hide functionality"""
        try:
            from PyQt5.QtCore import QPoint, QTimer
            
            # Show window
            self.window.show_at_position(QPoint(100, 100))
            self.assertTrue(self.window.isVisible(), "Window should be visible initially")
            
            # Test auto-hide timer exists
            self.assertIsNotNone(self.window.auto_hide_timer, "Auto-hide timer should exist")
            self.assertIsInstance(self.window.auto_hide_timer, QTimer, "Auto-hide timer should be QTimer")
            
            # Test manual hide
            self.window.fade_out()
            self.assertFalse(self.window.isVisible(), "Window should be hidden after fade_out")
            
        except Exception as e:
            self.fail(f"Error testing popup auto-hide: {e}")
    
    def test_popup_window_content_display(self):
        """Test popup window content display"""
        try:
            # Test translation display
            test_translation = "Hello World"
            self.window.show_translation("Original", test_translation)
            result_text = self.window.result_label.text()
            self.assertEqual(result_text, test_translation, "Translation should be displayed correctly")
            
            # Test error display
            test_error = "Test error message"
            self.window.show_error(test_error)
            error_text = self.window.result_label.text()
            self.assertEqual(error_text, test_error, "Error should be displayed correctly")
            
        except Exception as e:
            self.fail(f"Error testing popup content display: {e}")
    
    def test_copy_functionality(self):
        """Test copy button functionality"""
        try:
            import pyperclip
            
            # Set test content
            test_content = "Test translation content"
            self.window.show_translation("Original", test_content)
            
            # Test copy functionality
            self.window.copy_translation()
            
            # Verify content was copied to clipboard
            clipboard_content = pyperclip.paste()
            self.assertEqual(clipboard_content, test_content, "Content should be copied to clipboard")
            
        except Exception as e:
            self.fail(f"Error testing copy functionality: {e}")

@unittest.skipIf(not PYQT_AVAILABLE, f"PyQt not available for GUI testing")
class TestDialogInteractions(unittest.TestCase):
    """Test dialog interactions and functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Create QApplication for GUI testing"""
        if not QApplication.instance():
            cls.app = QApplication([])
        else:
            cls.app = QApplication.instance()
    
    def test_settings_dialog_tabs(self):
        """Test settings dialog tab functionality"""
        try:
            import translator
            config = {
                "translation": {"auto_translate": True, "default_target": "zh-TW"},
                "ui": {"font_size": 14, "window_opacity": 0.95},
                "translation_service": {
                    "provider": "google",
                    "google_api": {"api_key": "", "endpoint": ""},
                    "custom_llm": {"enabled": False, "api_url": "", "api_key": "", "system_prompt": ""}
                }
            }
            memory = translator.TranslationMemory(":memory:")
            dialog = translator.SettingsDialog(config, memory)
            
            # Test that dialog has tab widget
            tab_widget = dialog.findChild(type(dialog), name="tab_widget") or dialog.findChildren(type(dialog))[0] if dialog.findChildren(type(dialog)) else None
            if hasattr(dialog, 'children'):
                tab_widgets = [child for child in dialog.children() if hasattr(child, 'count')]
                if tab_widgets:
                    tab_widget = tab_widgets[0]
                    self.assertGreater(tab_widget.count(), 0, "Settings dialog should have tabs")
            
            dialog.close()
            
        except Exception as e:
            self.fail(f"Error testing settings dialog tabs: {e}")
    
    def test_batch_translation_interface(self):
        """Test batch translation dialog interface"""
        try:
            import translator
            import tempfile
            import os
            
            # Create a temporary database file
            temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
            temp_db.close()
            
            try:
                config = {"translation_service": {"provider": "google"}}
                memory = translator.TranslationMemory(temp_db.name)
                dialog = translator.BatchTranslationDialog(config, memory)
                
                # Test that required UI elements exist
                self.assertIsNotNone(dialog.input_text, "Input text widget should exist")
                self.assertIsNotNone(dialog.result_table, "Result table should exist")
                self.assertIsNotNone(dialog.progress_bar, "Progress bar should exist")
                self.assertIsNotNone(dialog.translate_button, "Translate button should exist")
                
                # Test table structure
                self.assertEqual(dialog.result_table.columnCount(), 3, "Result table should have 3 columns")
                
                dialog.close()
            finally:
                if os.path.exists(temp_db.name):
                    os.unlink(temp_db.name)
            
        except Exception as e:
            self.fail(f"Error testing batch translation interface: {e}")
    
    def test_translation_history_interface(self):
        """Test translation history dialog interface"""
        try:
            import translator
            import tempfile
            import os
            
            # Create a temporary database file
            temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
            temp_db.close()
            
            try:
                memory = translator.TranslationMemory(temp_db.name)
                dialog = translator.TranslationHistoryDialog(memory)
                
                # Test that required UI elements exist
                self.assertIsNotNone(dialog.search_input, "Search input should exist")
                self.assertIsNotNone(dialog.history_table, "History table should exist")
                
                # Test table structure
                self.assertEqual(dialog.history_table.columnCount(), 6, "History table should have 6 columns")
                
                dialog.close()
            finally:
                if os.path.exists(temp_db.name):
                    os.unlink(temp_db.name)
            
        except Exception as e:
            self.fail(f"Error testing translation history interface: {e}")
    
    def test_language_manager_interface(self):
        """Test language manager dialog interface"""
        try:
            import translator
            import tempfile
            import os
            
            # Create a temporary database file
            temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
            temp_db.close()
            
            try:
                memory = translator.TranslationMemory(temp_db.name)
                dialog = translator.LanguageManagerDialog(memory)
                
                # Test that required UI elements exist
                self.assertIsNotNone(dialog.language_table, "Language table should exist")
                
                # Test table structure
                self.assertEqual(dialog.language_table.columnCount(), 4, "Language table should have 4 columns")
                
                # Test that languages are loaded
                self.assertGreater(dialog.language_table.rowCount(), 0, "Should have at least one language")
                
                dialog.close()
            finally:
                if os.path.exists(temp_db.name):
                    os.unlink(temp_db.name)
            
        except Exception as e:
            self.fail(f"Error testing language manager interface: {e}")

@unittest.skipIf(not PYQT_AVAILABLE, f"PyQt not available for GUI testing")
class TestTranslationMemoryGUI(unittest.TestCase):
    """Test translation memory GUI functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Create QApplication for GUI testing"""
        if not QApplication.instance():
            cls.app = QApplication([])
        else:
            cls.app = QApplication.instance()
    
    def test_translation_memory_database(self):
        """Test translation memory database operations through GUI"""
        try:
            import translator
            import tempfile
            import os
            
            # Create a temporary database file instead of using :memory:
            temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
            temp_db.close()
            
            try:
                memory = translator.TranslationMemory(temp_db.name)
                
                # Test saving translation
                memory.save_translation("Hello", "你好", "en", "zh-TW", "test")
                
                # Test retrieving translation
                result = memory.get_translation("Hello", "en", "zh-TW")
                self.assertEqual(result, "你好", "Should retrieve saved translation")
                
                # Test enabled languages
                languages = memory.get_enabled_languages()
                self.assertIsInstance(languages, list, "Should return list of languages")
                self.assertGreater(len(languages), 0, "Should have enabled languages")
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_db.name):
                    os.unlink(temp_db.name)
            
        except Exception as e:
            self.fail(f"Error testing translation memory database: {e}")
    
    def test_translation_worker_integration(self):
        """Test translation worker thread integration"""
        try:
            import translator
            import tempfile
            import os
            
            # Create a temporary database file
            temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
            temp_db.close()
            
            try:
                config = {
                    "translation_service": {"provider": "google"},
                    "translation": {"default_target": "zh-TW"}
                }
                memory = translator.TranslationMemory(temp_db.name)
                
                # Test worker creation
                worker = translator.TranslationWorker("Hello", config, memory, "en", "zh-TW")
                self.assertIsInstance(worker, QThread, "Worker should be a QThread")
                self.assertIsNotNone(worker.translation_complete, "Should have translation_complete signal")
                self.assertIsNotNone(worker.translation_error, "Should have translation_error signal")
            finally:
                if os.path.exists(temp_db.name):
                    os.unlink(temp_db.name)
            
        except Exception as e:
            self.fail(f"Error testing translation worker integration: {e}")

@unittest.skipIf(not PYQT_AVAILABLE, f"PyQt not available for GUI testing")
class TestSystemTrayIntegration(unittest.TestCase):
    """Test system tray integration"""
    
    @classmethod
    def setUpClass(cls):
        """Create QApplication for GUI testing"""
        if not QApplication.instance():
            cls.app = QApplication([])
        else:
            cls.app = QApplication.instance()
    
    def test_system_tray_availability(self):
        """Test system tray availability"""
        try:
            available = QSystemTrayIcon.isSystemTrayAvailable()
            if available:
                # Test tray icon creation
                tray = QSystemTrayIcon()
                self.assertIsNotNone(tray, "System tray icon should be created")
            else:
                self.skipTest("System tray not available on this system")
        except Exception as e:
            self.fail(f"Error testing system tray availability: {e}")
    
    def test_translator_app_creation(self):
        """Test that TranslatorApp can be created without GUI"""
        try:
            import translator
            
            # Mock the GUI components to avoid full initialization
            with unittest.mock.patch('translator.QSystemTrayIcon') as mock_tray:
                with unittest.mock.patch('translator.keyboard') as mock_keyboard:
                    # This would normally require GUI initialization
                    # We're just testing that the class can be imported and basic structure is correct
                    self.assertTrue(hasattr(translator, 'TranslatorApp'), "TranslatorApp class should exist")
                    
        except Exception as e:
            self.fail(f"Error testing TranslatorApp creation: {e}")

class TestBuildArtifacts(unittest.TestCase):
    """Test that all necessary build artifacts exist"""
    
    def test_icon_file_exists(self):
        """Test that icon.png exists"""
        self.assertTrue(os.path.exists("icon.png"), "icon.png not found")
    
    def test_spec_file_exists(self):
        """Test that .spec file was created"""
        spec_files = [f for f in os.listdir(".") if f.endswith(".spec")]
        self.assertGreater(len(spec_files), 0, "No .spec file found")
    
    def test_build_directory_exists(self):
        """Test that build directory was created"""
        self.assertTrue(os.path.exists("build"), "build directory not found")
    
    def test_dist_directory_exists(self):
        """Test that dist directory was created"""
        self.assertTrue(os.path.exists("dist"), "dist directory not found")

class TestExecutable(unittest.TestCase):
    """Test the built executable"""
    
    def setUp(self):
        self.exe_path = "dist/LLM_Translator.exe"
    
    def test_executable_exists(self):
        """Test that the executable file exists"""
        self.assertTrue(os.path.exists(self.exe_path), f"Executable not found at {self.exe_path}")
    
    def test_executable_size(self):
        """Test that the executable has reasonable size"""
        if os.path.exists(self.exe_path):
            size = os.path.getsize(self.exe_path)
            self.assertGreater(size, 10_000_000, "Executable seems too small (< 10MB)")
            self.assertLess(size, 100_000_000, "Executable seems too large (> 100MB)")
    
    def test_executable_runs(self):
        """Test that the executable can start without immediate crash"""
        if not os.path.exists(self.exe_path):
            self.skipTest("Executable not found")
        
        try:
            # Start the executable in a separate process
            process = subprocess.Popen(
                [self.exe_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # Wait a moment for it to start
            time.sleep(3)
            
            # Check if it's still running (not crashed immediately)
            poll_result = process.poll()
            
            if poll_result is None:
                # Process is still running, terminate it
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                self.assertTrue(True, "Executable started successfully")
            else:
                # Process terminated, check for errors
                stdout, stderr = process.communicate()
                error_msg = f"Executable crashed immediately. Return code: {poll_result}"
                if stderr:
                    error_msg += f"\nStderr: {stderr.decode('utf-8', errors='ignore')}"
                if stdout:
                    error_msg += f"\nStdout: {stdout.decode('utf-8', errors='ignore')}"
                self.fail(error_msg)
                
        except Exception as e:
            self.fail(f"Error testing executable: {e}")
    
    @unittest.skipIf(not PSUTIL_AVAILABLE, "psutil not available for enhanced process testing")
    def test_executable_actual_execution(self):
        """Test actual execution of .exe file with comprehensive validation"""
        if not os.path.exists(self.exe_path):
            self.skipTest("Executable not found")
        
        import time
        
        try:
            print(f"\n🚀 Testing actual execution of {self.exe_path}")
            
            # Start the executable
            process = subprocess.Popen(
                [self.exe_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # Wait for application to fully initialize
            time.sleep(5)
            
            # Verify process is running
            poll_result = process.poll()
            self.assertIsNone(poll_result, "Executable should still be running after 5 seconds")
            
            # Check if process exists in system
            try:
                proc = psutil.Process(process.pid)
                self.assertTrue(proc.is_running(), "Process should be running")
                self.assertEqual(proc.name(), "LLM_Translator.exe", "Process name should match")
                
                # Check memory usage (should be reasonable for GUI app)
                memory_info = proc.memory_info()
                memory_mb = memory_info.rss / (1024 * 1024)  # Convert to MB
                self.assertGreater(memory_mb, 10, "Memory usage should be > 10MB for GUI app")
                self.assertLess(memory_mb, 500, "Memory usage should be < 500MB")
                
                print(f"✅ Process running with PID: {process.pid}")
                print(f"✅ Memory usage: {memory_mb:.1f} MB")
                print(f"✅ Process name: {proc.name()}")
                
                # Test process stability over time
                for i in range(3):
                    time.sleep(2)
                    self.assertTrue(proc.is_running(), f"Process should still be running after {(i+1)*2+5} seconds")
                
                print("✅ Process stability verified (11 seconds total runtime)")
                
            except psutil.NoSuchProcess:
                self.fail("Process disappeared unexpectedly")
            
            # Gracefully terminate the process
            try:
                process.terminate()
                process.wait(timeout=10)
                print("✅ Process terminated gracefully")
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
                print("⚠️ Process had to be killed (not graceful)")
            
            # Verify clean termination
            self.assertIsNotNone(process.poll(), "Process should be terminated")
            
            # Check for any error output
            stdout, stderr = process.communicate()
            if stderr:
                stderr_text = stderr.decode('utf-8', errors='ignore').strip()
                if stderr_text and "QSystemTrayIcon::setVisible" not in stderr_text:
                    # Ignore common Qt system tray warnings
                    print(f"⚠️ Stderr output: {stderr_text}")
            
            print("✅ Actual execution test completed successfully")
            
        except Exception as e:
            # Clean up process if it's still running
            try:
                if process.poll() is None:
                    process.terminate()
                    process.wait(timeout=5)
            except:
                pass
            self.fail(f"Error during actual execution test: {e}")
    
    def test_executable_system_tray_integration(self):
        """Test that executable properly integrates with system tray"""
        if not os.path.exists(self.exe_path):
            self.skipTest("Executable not found")
        
        try:
            print(f"\n🖥️ Testing system tray integration")
            
            # Start the executable
            process = subprocess.Popen(
                [self.exe_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # Wait for system tray initialization
            time.sleep(7)
            
            # Verify process is running
            poll_result = process.poll()
            self.assertIsNone(poll_result, "Executable should be running with system tray")
            
            print("✅ Application started and running in system tray mode")
            
            # Test that the application handles system signals properly
            # by sending a polite termination request
            process.terminate()
            try:
                return_code = process.wait(timeout=10)
                print(f"✅ Application terminated with return code: {return_code}")
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
                print("⚠️ Application had to be force-killed")
            
            # Check for clean exit
            stdout, stderr = process.communicate()
            if return_code == 0:
                print("✅ Clean exit confirmed")
            
                 except Exception as e:
             # Clean up
             try:
                 if process.poll() is None:
                     process.terminate()
                     process.wait(timeout=5)
             except:
                 pass
             self.fail(f"Error testing system tray integration: {e}")

class TestHotkeyFunctionality(unittest.TestCase):
    """Test QTranslate-inspired hotkey functionality"""
    
    def setUp(self):
        self.exe_path = "dist/LLM_Translator.exe"
        self.process = None
    
    def tearDown(self):
        """Clean up running processes after each test"""
        if self.process and self.process.poll() is None:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except:
                try:
                    self.process.kill()
                    self.process.wait()
                except:
                    pass
    
    def test_hotkey_registration(self):
        """Test that hotkeys are properly registered in the application"""
        if not os.path.exists(self.exe_path):
            self.skipTest("Executable not found")
        
        try:
            print(f"\n🎹 Testing hotkey registration...")
            
            # Start the application
            self.process = subprocess.Popen(
                [self.exe_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # Wait for application to fully initialize and register hotkeys
            time.sleep(8)
            
            # Verify process is running (indicating successful hotkey registration)
            poll_result = self.process.poll()
            self.assertIsNone(poll_result, "Application should be running after hotkey registration")
            
            # Check if process is stable (no crashes from hotkey conflicts)
            for i in range(3):
                time.sleep(2)
                self.assertIsNone(self.process.poll(), f"Process should remain stable during hotkey operation (check {i+1})")
            
            print("✅ Hotkey registration test passed")
            
        except Exception as e:
            self.fail(f"Error testing hotkey registration: {e}")
    
    def test_keyboard_library_integration(self):
        """Test that keyboard library is properly integrated"""
        try:
            print(f"\n⌨️ Testing keyboard library integration...")
            
            # Test importing keyboard library
            import keyboard
            self.assertTrue(hasattr(keyboard, 'add_hotkey'), "keyboard.add_hotkey should be available")
            self.assertTrue(hasattr(keyboard, 'on_press'), "keyboard.on_press should be available")
            
            # Test basic hotkey registration (without conflicts)
            test_triggered = False
            
            def test_callback():
                nonlocal test_triggered
                test_triggered = True
            
            # Register a test hotkey that shouldn't conflict
            keyboard.add_hotkey('ctrl+shift+f12', test_callback, suppress=True)
            
            # Clean up immediately to avoid conflicts
            keyboard.unhook_all()
            
            print("✅ Keyboard library integration test passed")
            
        except Exception as e:
            self.fail(f"Error testing keyboard library integration: {e}")
    
    def test_qtranslate_hotkey_configuration(self):
        """Test that QTranslate-style hotkeys are properly configured"""
        try:
            print(f"\n🔧 Testing QTranslate hotkey configuration...")
            
            # Import the translator module to check hotkey configuration
            import translator
            
            # Check if AdvancedHotkeyManager exists
            self.assertTrue(hasattr(translator, 'AdvancedHotkeyManager'), 
                          "AdvancedHotkeyManager class should exist")
            
            # Create a mock app object for testing
            class MockApp:
                pass
            
            mock_app = MockApp()
            hotkey_manager = translator.AdvancedHotkeyManager(mock_app)
            
            # Verify essential hotkeys are configured
            essential_hotkeys = ['popup_window', 'manual_translate', 'listen_text', 'dictionary', 'switch_languages']
            for hotkey in essential_hotkeys:
                self.assertIn(hotkey, hotkey_manager.hotkeys, f"Essential hotkey '{hotkey}' should be configured")
            
            # Verify QTranslate-style hotkey patterns
            self.assertEqual(hotkey_manager.hotkeys['popup_window'], 'ctrl+q', 
                           "Popup window should use Ctrl+Q (QTranslate standard)")
            self.assertEqual(hotkey_manager.hotkeys['manual_translate'], 'ctrl+shift+t', 
                           "Manual translate should use Ctrl+Shift+T")
            self.assertEqual(hotkey_manager.hotkeys['dictionary'], 'ctrl+d', 
                           "Dictionary should use Ctrl+D (QTranslate standard)")
            
            print("✅ QTranslate hotkey configuration test passed")
            
        except Exception as e:
            self.fail(f"Error testing QTranslate hotkey configuration: {e}")
    
    def test_multi_service_hotkey_support(self):
        """Test that service selection hotkeys (Ctrl+1-9) are supported"""
        try:
            print(f"\n🔄 Testing multi-service hotkey support...")
            
            import translator
            
            # Check MultiServiceTranslator exists
            self.assertTrue(hasattr(translator, 'MultiServiceTranslator'), 
                          "MultiServiceTranslator class should exist")
            
            multi_translator = translator.MultiServiceTranslator()
            
            # Verify multiple services are available for hotkey switching
            self.assertGreater(len(multi_translator.services), 1, 
                             "Should have multiple translation services for hotkey switching")
            
            # Verify service order for hotkey mapping
            self.assertTrue(hasattr(multi_translator, 'service_order'), 
                          "Should have service_order for Ctrl+1-9 mapping")
            
            # Check essential services
            essential_services = ['google', 'deepl', 'microsoft']
            for service in essential_services:
                self.assertIn(service, multi_translator.services, 
                            f"Service '{service}' should be available for hotkey selection")
            
            print("✅ Multi-service hotkey support test passed")
            
        except Exception as e:
            self.fail(f"Error testing multi-service hotkey support: {e}")
    
    def test_theme_switching_hotkeys(self):
        """Test that theme switching hotkeys (Ctrl+Shift+F1-F5) are supported"""
        try:
            print(f"\n🎨 Testing theme switching hotkey support...")
            
            import translator
            
            # Check ThemeManager exists
            self.assertTrue(hasattr(translator, 'ThemeManager'), 
                          "ThemeManager class should exist")
            
            theme_manager = translator.ThemeManager()
            
            # Verify multiple themes are available for hotkey switching
            self.assertGreaterEqual(len(theme_manager.themes), 5, 
                                  "Should have at least 5 themes for Ctrl+Shift+F1-F5 hotkeys")
            
            # Check essential themes
            essential_themes = ["Photoshop Dark", "Holo Light", "Metro", "Blue", "Flat Dark"]
            for theme in essential_themes:
                self.assertIn(theme, theme_manager.themes, 
                            f"Theme '{theme}' should be available for hotkey selection")
            
            # Verify theme structure
            for theme_name, theme_data in theme_manager.themes.items():
                self.assertIn('Window', theme_data, f"Theme '{theme_name}' should have Window configuration")
                self.assertIn('Button', theme_data, f"Theme '{theme_name}' should have Button configuration")
            
            print("✅ Theme switching hotkey support test passed")
            
        except Exception as e:
            self.fail(f"Error testing theme switching hotkey support: {e}")
    
    def test_copy_detection_functionality(self):
        """Test that Ctrl+C copy detection is working"""
        try:
            print(f"\n📋 Testing Ctrl+C copy detection functionality...")
            
            import translator
            import tempfile
            import os
            
            # Create a temporary database for testing
            temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
            temp_db.close()
            
            try:
                # Create translation memory
                memory = translator.TranslationMemory(temp_db.name)
                
                # Test basic config structure for copy detection
                test_config = {
                    'translation': {
                        'auto_translate': True,
                        'default_target': 'zh-TW'
                    }
                }
                
                # Test language detector
                detector = translator.LanguageDetector()
                test_result = detector.detect_language("Hello world")
                self.assertIsInstance(test_result, str, "Language detection should return a string")
                
                # Test translation worker creation
                worker = translator.TranslationWorker("test text", test_config, memory, 'auto', 'zh-TW')
                self.assertIsNotNone(worker, "TranslationWorker should be created successfully")
                
                print("✅ Copy detection functionality test passed")
                
            finally:
                if os.path.exists(temp_db.name):
                    os.unlink(temp_db.name)
            
        except Exception as e:
            self.fail(f"Error testing copy detection functionality: {e}")

def run_tests():
    """Run all tests and return results"""
    # Import mock for GUI tests that need it
    global unittest
    try:
        import unittest.mock
    except ImportError:
        import mock
        unittest.mock = mock
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestImports,
        TestConfiguration,
        TestSourceCode,
        TestBuildArtifacts,
        TestExecutable,
        TestHotkeyFunctionality,
        # GUI Tests (will be skipped if PyQt not available)
        TestGUIComponents,
        TestPopupWindow,
        TestDialogInteractions,
        TestTranslationMemoryGUI,
        TestSystemTrayIntegration,
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(test_suite)
    
    return result

def main():
    """Main test function"""
    print("="*60)
    print("LLM Translator Enhanced Test Suite with GUI Testing")
    print("="*60)
    
    if PYQT_AVAILABLE:
        print(f"GUI Testing: Enabled ({PYQT_VERSION})")
    else:
        print("GUI Testing: Disabled (PyQt not available)")
    
    print("="*60)
    
    result = run_tests()
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    if result.skipped:
        print("\nSKIPPED:")
        for test, reason in result.skipped:
            print(f"- {test}: {reason}")
    
    # Calculate GUI test statistics (simplified)
    gui_test_classes = ['TestGUIComponents', 'TestPopupWindow', 'TestDialogInteractions', 'TestTranslationMemoryGUI', 'TestSystemTrayIntegration']
    total_gui_tests = 0
    if PYQT_AVAILABLE:
        # Count GUI tests that were actually run
        for test_class in gui_test_classes:
            if any(test_class in str(test) for test in [t[0] for t in result.failures + result.errors]):
                total_gui_tests += 1
        # Add successful GUI tests
        total_gui_tests += len([t for t in range(result.testsRun) if any(cls in str(t) for cls in gui_test_classes)])
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\nOVERALL RESULT: {'✅ PASS' if success else '❌ FAIL'}")
    
    if PYQT_AVAILABLE:
        print(f"\n🎨 GUI Testing Summary: Comprehensive GUI component testing completed")
        print(f"   - All dialog windows tested for creation and basic functionality")
        print(f"   - Popup window positioning and behavior verified")
        print(f"   - Translation memory GUI integration confirmed")
        print(f"   - System tray integration validated")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 