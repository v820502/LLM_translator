import os
import shutil
import platform
import subprocess

def build_exe():
    print("Starting build process...")
    
    # 確保圖標存在
    if not os.path.exists('icon.png'):
        print("Generating icon...")
        try:
            from PIL import Image, ImageDraw
            # 創建一個 64x64 的圖像
            img = Image.new('RGBA', (64, 64), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            # 繪製一個簡單的翻譯圖標
            draw.rectangle([10, 10, 54, 54], fill='#4a90e2', outline='#2171c7', width=2)
            # 保存圖標
            img.save('icon.png')
            print("Icon generated successfully!")
        except Exception as e:
            print(f"Error generating icon: {e}")
            return

    # 清理之前的構建
    print("Cleaning previous builds...")
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('LLM_Translator.spec'):
        os.remove('LLM_Translator.spec')

    print("Starting PyInstaller with Wine...")
    
    # 使用 wine 運行 PyInstaller
    pyinstaller_cmd = [
        'wine', 'pyinstaller',
        '--name=LLM_Translator',
        '--windowed',
        '--noconsole',
        '--icon=icon.png',
        '--add-data=icon.png;.',
        '--add-data=config.json;.',
        '--onefile',
        '--clean',
        '--noconfirm',
        'translator.py'
    ]

    try:
        # 執行打包
        subprocess.run(pyinstaller_cmd, check=True)
        print("\nBuild completed successfully!")
        
        # 檢查輸出文件
        exe_path = os.path.join('dist', 'LLM_Translator.exe')
        if os.path.exists(exe_path):
            print(f"Windows executable created at: {exe_path}")
            print("\nTo test the application:")
            print("1. Copy the .exe file to a Windows system")
            print("2. Run the executable")
            print("3. Check if the icon appears in the system tray")
            print("4. Select some text and press Ctrl+C to test translation")
        else:
            print("Error: Windows executable was not created!")
            
    except subprocess.CalledProcessError as e:
        print(f"\nError during build: {e}")
    except Exception as e:
        print(f"\nUnexpected error: {e}")

if __name__ == '__main__':
    build_exe() 