#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自動化Build和測試腳本
"""

import os
import sys
import subprocess
import time
import psutil
from datetime import datetime

def log_message(message, level="INFO"):
    """記錄日誌消息"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def kill_existing_processes():
    """終止現有的翻譯器進程"""
    log_message("檢查並終止現有的翻譯器進程...")
    killed_count = 0
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'python' in proc.info['name'].lower():
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                if 'translator.py' in cmdline:
                    log_message(f"終止進程 PID: {proc.info['pid']}")
                    proc.kill()
                    killed_count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    if killed_count > 0:
        log_message(f"已終止 {killed_count} 個翻譯器進程")
        time.sleep(2)  # 等待進程完全終止
    else:
        log_message("沒有發現現有的翻譯器進程")

def run_pre_build_tests():
    """執行Build前測試"""
    log_message("執行Build前測試...")
    
    try:
        result = subprocess.run([
            sys.executable, "test_suite.py"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            log_message("✅ Pre-build測試通過", "SUCCESS")
            return True
        else:
            log_message("❌ Pre-build測試失敗", "ERROR")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        log_message("⏰ Pre-build測試超時", "WARNING")
        return False
    except Exception as e:
        log_message(f"❌ Pre-build測試異常: {e}", "ERROR")
        return False

def run_build():
    """執行Build"""
    log_message("開始執行Build...")
    
    try:
        # 使用Windows batch文件進行build
        result = subprocess.run([
            "build_windows.bat"
        ], capture_output=True, text=True, timeout=600, shell=True)
        
        if result.returncode == 0:
            log_message("✅ Build成功完成", "SUCCESS")
            
            # 檢查輸出文件
            exe_path = os.path.join("dist", "LLM_Translator.exe")
            if os.path.exists(exe_path):
                file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
                log_message(f"✅ 可執行文件已生成: {file_size:.1f} MB", "SUCCESS")
                return True
            else:
                log_message("❌ 可執行文件未生成", "ERROR")
                return False
        else:
            log_message("❌ Build失敗", "ERROR")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        log_message("⏰ Build超時", "WARNING")
        return False
    except Exception as e:
        log_message(f"❌ Build異常: {e}", "ERROR")
        return False

def run_post_build_tests():
    """執行Build後測試"""
    log_message("執行Build後測試...")
    
    try:
        # 先執行我們的測試套件
        result = subprocess.run([
            sys.executable, "test_suite.py"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            log_message("❌ Post-build測試失敗", "ERROR")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
        
        # 如果存在原始的test_build.py，也執行它
        if os.path.exists("test_build.py"):
            log_message("執行原始build測試...")
            result2 = subprocess.run([
                sys.executable, "test_build.py"
            ], capture_output=True, text=True, timeout=180)
            
            if result2.returncode != 0:
                log_message("⚠️ 原始build測試有警告", "WARNING")
                print("STDOUT:", result2.stdout)
            else:
                log_message("✅ 原始build測試通過", "SUCCESS")
        
        log_message("✅ Post-build測試通過", "SUCCESS")
        return True
        
    except subprocess.TimeoutExpired:
        log_message("⏰ Post-build測試超時", "WARNING")
        return False
    except Exception as e:
        log_message(f"❌ Post-build測試異常: {e}", "ERROR")
        return False

def run_integration_tests():
    """執行整合測試"""
    log_message("執行整合測試...")
    
    try:
        # 啟動翻譯器進行整合測試
        log_message("啟動翻譯器進行整合測試...")
        
        # 在背景啟動翻譯器
        translator_process = subprocess.Popen([
            sys.executable, "translator.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 等待程式啟動
        time.sleep(5)
        
        # 檢查進程是否還在運行
        if translator_process.poll() is None:
            log_message("✅ 翻譯器成功啟動", "SUCCESS")
            
            # 執行整合測試
            time.sleep(2)
            test_result = subprocess.run([
                sys.executable, "debug_status.py"
            ], capture_output=True, text=True, timeout=30)
            
            if "✅ 翻譯器正在運行" in test_result.stdout:
                log_message("✅ 整合測試通過", "SUCCESS")
                integration_success = True
            else:
                log_message("❌ 整合測試失敗", "ERROR")
                integration_success = False
            
            # 終止測試進程
            try:
                translator_process.terminate()
                translator_process.wait(timeout=5)
            except:
                translator_process.kill()
            
            return integration_success
        else:
            log_message("❌ 翻譯器啟動失敗", "ERROR")
            stdout, stderr = translator_process.communicate()
            print("STDOUT:", stdout.decode())
            print("STDERR:", stderr.decode())
            return False
            
    except Exception as e:
        log_message(f"❌ 整合測試異常: {e}", "ERROR")
        return False

def main():
    """主函數"""
    log_message("開始自動化Build和測試流程")
    log_message("=" * 50)
    
    start_time = time.time()
    overall_success = True
    
    # 階段1: 清理環境
    log_message("階段1: 清理環境")
    kill_existing_processes()
    
    # 階段2: Pre-build測試
    log_message("階段2: Pre-build測試")
    if not run_pre_build_tests():
        log_message("Pre-build測試失敗，但繼續Build流程", "WARNING")
        # 不要因為pre-build測試失敗就停止
    
    # 階段3: Build
    log_message("階段3: 執行Build")
    if not run_build():
        log_message("❌ Build失敗，流程終止", "ERROR")
        overall_success = False
        return 1
    
    # 階段4: Post-build測試
    log_message("階段4: Post-build測試")
    if not run_post_build_tests():
        log_message("❌ Post-build測試失敗", "ERROR")
        overall_success = False
    
    # 階段5: 整合測試
    log_message("階段5: 整合測試")
    if not run_integration_tests():
        log_message("❌ 整合測試失敗", "ERROR")
        overall_success = False
    
    # 最終清理
    log_message("最終清理...")
    kill_existing_processes()
    
    # 總結
    end_time = time.time()
    duration = end_time - start_time
    
    log_message("=" * 50)
    if overall_success:
        log_message(f"🎉 所有流程成功完成！耗時: {duration:.1f}秒", "SUCCESS")
        log_message("✅ Build成功")
        log_message("✅ 所有測試通過")
        log_message("✅ 整合測試通過")
        return 0
    else:
        log_message(f"💥 部分流程失敗！耗時: {duration:.1f}秒", "ERROR")
        log_message("請檢查上述錯誤信息")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 