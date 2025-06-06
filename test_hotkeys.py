#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Hotkey Functionality Test Script
Tests the QTranslate-inspired hotkeys in the running LLM Translator
"""

import time
import sys
import pyperclip
import subprocess
import os

def test_copy_detection():
    """Test Ctrl+C copy detection functionality"""
    print("\n=== Testing Ctrl+C Copy Detection ===")
    
    # Set test text in clipboard
    test_texts = [
        "Hello, world!",
        "This is a test sentence for translation.",
        "Testing copy detection feature",
        "你好世界",
        "Bonjour le monde"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📋 Test {i}/5: Testing with text: '{text}'")
        
        # Set text to clipboard (simulating Ctrl+C)
        pyperclip.copy(text)
        print(f"✅ Text copied to clipboard")
        
        # Wait for translation detection
        print("⏳ Waiting 3 seconds for auto-translation...")
        time.sleep(3)
        
        print(f"🎯 Text should have been detected and translation popup should appear")

def test_application_status():
    """Test if the application is running and responsive"""
    print("\n=== Testing Application Status ===")
    
    try:
        # Check if LLM_Translator processes are running
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq LLM_Translator.exe'], 
                              capture_output=True, text=True, shell=True)
        
        if "LLM_Translator.exe" in result.stdout:
            print("✅ LLM_Translator application is running")
            
            # Count processes
            lines = result.stdout.split('\n')
            process_count = sum(1 for line in lines if 'LLM_Translator.exe' in line)
            print(f"📊 Found {process_count} LLM_Translator process(es)")
            
            return True
        else:
            print("❌ LLM_Translator application is NOT running")
            return False
            
    except Exception as e:
        print(f"⚠️ Error checking application status: {e}")
        return False

def test_hotkey_instructions():
    """Provide instructions for manual hotkey testing"""
    print("\n=== Manual Hotkey Testing Instructions ===")
    print("🎹 Please test the following hotkeys manually:")
    print()
    print("Core Translation Hotkeys:")
    print("  Ctrl+Q          - Popup translation (should show translation window)")
    print("  Ctrl+Shift+T    - Manual translate (should translate selected text)")
    print("  Ctrl+E          - Text-to-speech (should read text aloud)")
    print("  Ctrl+D          - Dictionary lookup (should open dictionary)")
    print("  Ctrl+I          - Switch languages (should swap source/target)")
    print()
    print("Service Selection (Ctrl+1-9):")
    print("  Ctrl+1          - Switch to Google Translate")
    print("  Ctrl+2          - Switch to DeepL Translator") 
    print("  Ctrl+3          - Switch to Microsoft Translator")
    print("  Ctrl+4          - Switch to Yandex Translate")
    print("  Ctrl+5          - Switch to Baidu Translate")
    print()
    print("Theme Switching (Ctrl+Shift+F1-F5):")
    print("  Ctrl+Shift+F1   - Photoshop Dark theme")
    print("  Ctrl+Shift+F2   - Holo Light theme")
    print("  Ctrl+Shift+F3   - Metro theme")
    print("  Ctrl+Shift+F4   - Blue theme")
    print("  Ctrl+Shift+F5   - Flat Dark theme")
    print()
    print("Advanced Features:")
    print("  Ctrl+Shift+O    - OCR translation (screen capture)")
    print("  Ctrl+Shift+S    - Speech input (voice recognition)")
    print("  Ctrl+H          - Translation history")
    print("  Ctrl+Shift+M    - Mouse mode toggle")

def main():
    """Main test function"""
    print("🔧 LLM Translator Hotkey Functionality Test")
    print("=" * 50)
    
    # Test 1: Check if application is running
    if not test_application_status():
        print("\n❌ Cannot proceed with tests - application is not running")
        print("💡 Please start the LLM_Translator.exe first")
        return 1
    
    # Test 2: Test copy detection (automated)
    test_copy_detection()
    
    # Test 3: Provide manual testing instructions
    test_hotkey_instructions()
    
    print("\n" + "=" * 50)
    print("✅ Automated tests completed!")
    print("🎯 Please test the manual hotkeys listed above")
    print("📝 Check system tray notifications for hotkey confirmations")
    print("💡 Look for translation popups when using Ctrl+C and Ctrl+Q")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 