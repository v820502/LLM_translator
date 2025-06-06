import os
import json

def test_basic_setup():
    """測試基本設置是否正確"""
    print("Testing LLM Translator basic setup...")
    
    # 檢查必要檔案
    required_files = ['translator.py', 'config.json', 'requirements.txt']
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"❌ {file} missing")
            return False
    
    # 檢查配置檔案
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        print("✓ config.json is valid JSON")
        
        # 檢查必要的配置項目
        required_sections = ['api', 'translation', 'ui', 'hotkeys']
        for section in required_sections:
            if section in config:
                print(f"✓ Config section '{section}' found")
            else:
                print(f"❌ Config section '{section}' missing")
                
    except Exception as e:
        print(f"❌ Error reading config.json: {e}")
        return False
    
    # 檢查圖標
    if os.path.exists('icon.png'):
        print("✓ icon.png exists")
    else:
        print("⚠ icon.png not found, will be generated during build")
    
    # 檢查打包檔案
    if os.path.exists('build_windows.bat'):
        print("✓ build_windows.bat exists for Windows building")
    
    print("\n🎉 Basic setup test completed successfully!")
    print("\nNext steps:")
    print("1. Copy all files to a Windows system")
    print("2. Run 'build_windows.bat' on Windows to create the .exe")
    print("3. Test the .exe file")
    
    return True

if __name__ == '__main__':
    test_basic_setup() 