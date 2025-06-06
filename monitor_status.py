#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翻譯器狀態監控和調試工具
"""

import psutil
import time
import json
import sqlite3
import os
import pyperclip
import threading
from datetime import datetime

class TranslatorMonitor:
    def __init__(self):
        self.config_file = "config.json"
        self.db_file = "translation_memory.db"
        self.monitor_running = True
        
    def load_config(self):
        """載入配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 配置文件載入失敗: {e}")
            return None
    
    def check_process_status(self):
        """檢查翻譯器進程狀態"""
        python_processes = []
        translator_found = False
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'memory_info', 'cpu_percent']):
            try:
                if 'python' in proc.info['name'].lower():
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    if 'translator.py' in cmdline:
                        translator_found = True
                        memory_mb = proc.info['memory_info'].rss / 1024 / 1024
                        cpu_percent = proc.info['cpu_percent']
                        print(f"✅ 翻譯器進程運行中:")
                        print(f"   PID: {proc.info['pid']}")
                        print(f"   記憶體使用: {memory_mb:.1f} MB")
                        print(f"   CPU使用率: {cpu_percent:.1f}%")
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if not translator_found:
            print("❌ 翻譯器進程未找到")
            return False
    
    def check_database_status(self):
        """檢查資料庫狀態"""
        try:
            if not os.path.exists(self.db_file):
                print("❌ 翻譯記憶庫資料庫不存在")
                return False
                
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # 檢查表是否存在
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            print(f"✅ 資料庫連接正常，包含表格: {', '.join(tables)}")
            
            # 檢查翻譯記錄數量
            if 'translations' in tables:
                cursor.execute("SELECT COUNT(*) FROM translations")
                count = cursor.fetchone()[0]
                print(f"   翻譯記錄數量: {count}")
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ 資料庫檢查失敗: {e}")
            return False
    
    def check_clipboard_function(self):
        """檢查剪貼簿功能"""
        try:
            # 測試讀取剪貼簿
            current_content = pyperclip.paste()
            print(f"✅ 剪貼簿功能正常")
            print(f"   當前內容: {current_content[:50]}{'...' if len(current_content) > 50 else ''}")
            return True
        except Exception as e:
            print(f"❌ 剪貼簿功能異常: {e}")
            return False
    
    def check_config_validity(self):
        """檢查配置文件有效性"""
        config = self.load_config()
        if not config:
            return False
            
        required_keys = ['auto_translate', 'source_language', 'target_language', 'translation_service']
        missing_keys = [key for key in required_keys if key not in config]
        
        if missing_keys:
            print(f"❌ 配置文件缺少必要項目: {', '.join(missing_keys)}")
            return False
        
        print("✅ 配置文件結構正常")
        print(f"   自動翻譯: {'開啟' if config.get('auto_translate') else '關閉'}")
        print(f"   來源語言: {config.get('source_language', 'unknown')}")
        print(f"   目標語言: {config.get('target_language', 'unknown')}")
        print(f"   翻譯服務: {config.get('translation_service', 'unknown')}")
        
        return True
    
    def test_translation_function(self):
        """測試翻譯功能"""
        print("\n🧪 測試翻譯功能...")
        test_text = "Hello, world!"
        
        try:
            # 將測試文字放入剪貼簿
            pyperclip.copy(test_text)
            print(f"   已將測試文字放入剪貼簿: {test_text}")
            print("   請觀察是否出現翻譯窗口...")
            
            # 等待一段時間觀察結果
            time.sleep(3)
            
            # 檢查剪貼簿是否有變化
            new_content = pyperclip.paste()
            if new_content != test_text:
                print(f"   剪貼簿內容已變更: {new_content}")
            else:
                print("   剪貼簿內容未變更")
                
        except Exception as e:
            print(f"❌ 翻譯功能測試失敗: {e}")
    
    def run_continuous_monitor(self):
        """持續監控模式"""
        print("🔄 開始持續監控模式 (按 Ctrl+C 停止)")
        
        try:
            while self.monitor_running:
                print(f"\n--- {datetime.now().strftime('%H:%M:%S')} 狀態檢查 ---")
                
                # 檢查進程狀態
                process_ok = self.check_process_status()
                
                if not process_ok:
                    print("❗ 翻譯器進程已停止，請重新啟動")
                    break
                
                # 每30秒檢查一次
                time.sleep(30)
                
        except KeyboardInterrupt:
            print("\n🛑 監控已停止")
    
    def run_full_check(self):
        """執行完整的狀態檢查"""
        print("🔍 執行翻譯器狀態全面檢查")
        print("=" * 50)
        
        # 1. 檢查進程狀態
        print("\n1. 檢查進程狀態:")
        process_ok = self.check_process_status()
        
        # 2. 檢查配置文件
        print("\n2. 檢查配置文件:")
        config_ok = self.check_config_validity()
        
        # 3. 檢查資料庫
        print("\n3. 檢查資料庫:")
        db_ok = self.check_database_status()
        
        # 4. 檢查剪貼簿功能
        print("\n4. 檢查剪貼簿功能:")
        clipboard_ok = self.check_clipboard_function()
        
        # 5. 測試翻譯功能
        if process_ok:
            self.test_translation_function()
        
        # 總結
        print("\n" + "=" * 50)
        print("📊 檢查結果總結:")
        print(f"   進程狀態: {'✅' if process_ok else '❌'}")
        print(f"   配置文件: {'✅' if config_ok else '❌'}")
        print(f"   資料庫: {'✅' if db_ok else '❌'}")
        print(f"   剪貼簿: {'✅' if clipboard_ok else '❌'}")
        
        overall_status = all([process_ok, config_ok, db_ok, clipboard_ok])
        print(f"\n整體狀態: {'✅ 正常' if overall_status else '❌ 有問題'}")
        
        return overall_status

def main():
    monitor = TranslatorMonitor()
    
    print("LLM翻譯器監控工具")
    print("選擇模式:")
    print("1. 完整狀態檢查")
    print("2. 持續監控模式")
    
    choice = input("請選擇 (1 或 2): ").strip()
    
    if choice == "1":
        monitor.run_full_check()
    elif choice == "2":
        monitor.run_continuous_monitor()
    else:
        print("自動執行完整狀態檢查...")
        monitor.run_full_check()

if __name__ == "__main__":
    main() 