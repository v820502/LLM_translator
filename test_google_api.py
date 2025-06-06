#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google翻譯API測試腳本
"""

import sys
import json
import time

def test_googletrans_library():
    """測試googletrans庫"""
    print("🔍 測試googletrans庫...")
    
    try:
        from googletrans import Translator
        translator = Translator()
        
        # 測試簡單翻譯
        test_cases = [
            ("Hello world", "zh-tw"),
            ("How are you?", "zh-tw"), 
            ("Good morning", "zh-tw"),
            ("你好", "en"),
            ("今天天氣很好", "en")
        ]
        
        for text, target_lang in test_cases:
            try:
                print(f"   測試: '{text}' -> {target_lang}")
                result = translator.translate(text, dest=target_lang)
                print(f"   結果: '{result.text}'")
                print(f"   檢測語言: {result.src}")
                print("   ✅ 成功")
                time.sleep(1)  # 避免請求過快
            except Exception as e:
                print(f"   ❌ 失敗: {e}")
                return False
        
        return True
        
    except ImportError:
        print("   ❌ googletrans庫未安裝")
        return False
    except Exception as e:
        print(f"   ❌ googletrans庫錯誤: {e}")
        return False

def test_alternative_google_api():
    """測試替代的Google翻譯方案"""
    print("\n🔍 測試替代Google翻譯方案...")
    
    try:
        import requests
        import urllib.parse
        
        def google_translate_free(text, target_lang='zh'):
            """使用免費的Google翻譯API"""
            # 這是一個簡化的方案，使用Google的網頁接口
            try:
                # 編碼文本
                encoded_text = urllib.parse.quote(text)
                
                # 構建URL（這個方法可能不穩定）
                url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={encoded_text}"
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    if result and len(result) > 0 and len(result[0]) > 0:
                        translation = result[0][0][0]
                        return translation
                    else:
                        return None
                else:
                    print(f"   HTTP錯誤: {response.status_code}")
                    return None
                    
            except Exception as e:
                print(f"   請求錯誤: {e}")
                return None
        
        # 測試替代方案
        test_cases = [
            ("Hello world", "zh"),
            ("How are you?", "zh"),
            ("你好", "en")
        ]
        
        for text, target_lang in test_cases:
            print(f"   測試: '{text}' -> {target_lang}")
            result = google_translate_free(text, target_lang)
            if result:
                print(f"   結果: '{result}'")
                print("   ✅ 成功")
            else:
                print("   ❌ 失敗")
                return False
            time.sleep(1)
        
        return True
        
    except Exception as e:
        print(f"   ❌ 替代方案錯誤: {e}")
        return False

def test_deepl_translate():
    """測試DeepL翻譯（如果可用）"""
    print("\n🔍 測試DeepL翻譯...")
    
    try:
        # 檢查DeepL是否可用（免費版）
        import requests
        
        def deepl_translate_free(text, target_lang='ZH'):
            """使用DeepL的免費翻譯"""
            try:
                url = "https://www2.deepl.com/jsonrpc"
                
                data = {
                    "jsonrpc": "2.0",
                    "method": "LMT_handle_jobs",
                    "params": {
                        "jobs": [{"kind": "default", "raw_en_sentence": text}],
                        "lang": {
                            "user_preferred_langs": ["ZH", "EN"],
                            "source_lang_user_selected": "auto",
                            "target_lang": target_lang
                        }
                    },
                    "id": 1
                }
                
                headers = {
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.post(url, json=data, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    if 'result' in result and 'translations' in result['result']:
                        translations = result['result']['translations']
                        if translations and len(translations) > 0:
                            return translations[0]['beams'][0]['postprocessed_sentence']
                
                return None
                
            except Exception as e:
                print(f"   DeepL請求錯誤: {e}")
                return None
        
        # 測試DeepL
        test_text = "Hello world"
        result = deepl_translate_free(test_text)
        if result:
            print(f"   測試: '{test_text}' -> 中文")
            print(f"   結果: '{result}'")
            print("   ✅ DeepL可用")
            return True
        else:
            print("   ❌ DeepL不可用")
            return False
            
    except Exception as e:
        print(f"   ❌ DeepL測試錯誤: {e}")
        return False

def get_current_config():
    """獲取當前配置"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"無法讀取配置文件: {e}")
        return None

def main():
    """主函數"""
    print("Google翻譯API測試工具")
    print("=" * 50)
    
    # 檢查當前配置
    config = get_current_config()
    if config:
        provider = config.get('translation_service', {}).get('provider', 'unknown')
        print(f"當前翻譯服務: {provider}")
        
        google_api_key = config.get('translation_service', {}).get('google_api', {}).get('api_key', '')
        if google_api_key:
            print("✅ Google API密鑰已設置")
        else:
            print("⚠️ Google API密鑰未設置，將使用免費方案")
    
    print()
    
    # 測試1: googletrans庫
    googletrans_ok = test_googletrans_library()
    
    # 測試2: 替代方案
    alternative_ok = test_alternative_google_api()
    
    # 測試3: DeepL（可選）
    deepl_ok = test_deepl_translate()
    
    # 總結
    print("\n" + "=" * 50)
    print("📊 測試結果總結:")
    print(f"   googletrans庫: {'✅ 可用' if googletrans_ok else '❌ 不可用'}")
    print(f"   替代Google方案: {'✅ 可用' if alternative_ok else '❌ 不可用'}")
    print(f"   DeepL方案: {'✅ 可用' if deepl_ok else '❌ 不可用'}")
    
    if googletrans_ok:
        print("\n💡 建議: 繼續使用googletrans庫")
        return 0
    elif alternative_ok:
        print("\n💡 建議: 切換到替代Google翻譯方案")
        return 1
    elif deepl_ok:
        print("\n💡 建議: 切換到DeepL翻譯")
        return 2
    else:
        print("\n❌ 所有翻譯方案都不可用！")
        print("建議檢查網絡連接或考慮使用付費API")
        return -1

if __name__ == "__main__":
    exit_code = main()
    print(f"\n退出代碼: {exit_code}")
    sys.exit(exit_code) 