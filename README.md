# LLM Translator

一個基於LLM的文字翻譯工具，類似於QTranslate的升級版本。

## 功能特點

- 系統托盤運行
- 自動檢測文字選取
- 即時翻譯彈出視窗
- 支持中英互譯

## 安裝要求

- Python 3.8+
- Windows 作業系統

## 開發環境設置

1. 克隆此倉庫
2. 安裝依賴：
```bash
pip install -r requirements.txt
```

3. 生成圖標：
```bash
python icon.py
```

4. 運行程式：
```bash
python translator.py
```

## 打包成執行檔

1. 確保已安裝所有依賴：
```bash
pip install -r requirements.txt
```

2. 運行打包腳本：
```bash
python build.py
```

3. 打包完成後，可執行檔將在 `dist` 目錄中生成

## 使用方法

1. 直接運行 `dist/LLM_Translator.exe`
2. 程式會在系統托盤顯示圖標
3. 選取任何文字後，會自動彈出翻譯視窗
4. 右鍵點擊托盤圖標可以：
   - 打開設置
   - 退出程式

## 注意事項

- 需要管理員權限才能監聽全局鍵盤事件
- 首次運行時可能需要允許程式在背景運行
- 確保系統已安裝 Visual C++ Redistributable 