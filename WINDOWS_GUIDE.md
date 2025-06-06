# LLM Translator - Windows 使用指南

## 📋 系統需求
- Windows 10 或更新版本
- 4GB RAM
- 100MB 可用磁碟空間
- 網路連線（用於 LLM API）

## 🚀 快速開始

### 方法一：使用預建的 .exe 檔案
1. 下載 `LLM_Translator.exe`
2. 直接運行執行檔
3. 檢查系統托盤是否出現圖標
4. 選取文字並按 Ctrl+C 測試翻譯功能

### 方法二：從源碼建置
1. **安裝 Python**
   - 下載並安裝 Python 3.8+ 從 https://python.org
   - 安裝時確保勾選 "Add Python to PATH"

2. **下載項目檔案**
   - translator.py
   - config.json
   - requirements.txt
   - icon.py
   - build_windows.bat

3. **建置執行檔**
   - 將所有檔案放在同一個資料夾
   - 雙擊運行 `build_windows.bat`
   - 等待建置完成
   - 在 `dist` 資料夾中找到 `LLM_Translator.exe`

## ⚙️ 設定

### 首次設定
1. 右鍵點擊系統托盤圖標
2. 選擇 "設置"
3. 輸入您的 LLM API 金鑰
4. 選擇偏好的語言對
5. 儲存設定

### API 支援
- OpenAI GPT-4/3.5
- Anthropic Claude
- 其他兼容的 LLM API

## 🔧 使用方法

### 基本翻譯
1. 在任何應用程式中選取文字
2. 按 Ctrl+C 複製文字
3. 翻譯視窗會自動彈出
4. 查看翻譯結果

### 系統托盤功能
- **左鍵點擊**：顯示/隱藏主視窗
- **右鍵點擊**：開啟功能表
  - 設置
  - 翻譯歷史
  - 退出

### 快速鍵
- `Ctrl+C`：翻譯選取的文字
- `Ctrl+Alt+S`：開啟設置
- `Ctrl+Alt+H`：顯示翻譯歷史
- `Esc`：關閉翻譯視窗

## 🔍 疑難排解

### 常見問題

**Q: 程式無法啟動**
A: 確保已安裝 Visual C++ Redistributable

**Q: 系統托盤沒有圖標**
A: 檢查 Windows 系統托盤設定，確保允許應用程式顯示圖標

**Q: 翻譯功能無效**
A: 
- 檢查網路連線
- 確認 API 金鑰正確
- 檢查 API 配額

**Q: 無法選取文字**
A: 
- 以系統管理員身分運行程式
- 檢查防毒軟體是否阻擋

### 日誌檔案
- 檢查 `translator.log` 檔案以獲取錯誤訊息
- 位置：程式所在資料夾

## 🛡️ 安全性
- API 金鑰使用加密儲存
- 不會收集或傳送個人資料
- 僅在翻譯時連接網路

## 📞 支援
如果遇到問題：
1. 檢查本指南的疑難排解部分
2. 查看 `translator.log` 檔案
3. 確保系統符合最低需求

## 🔄 更新
- 程式會自動檢查更新（可在設定中關閉）
- 手動更新：下載新版本 .exe 檔案替換舊版本

---

*享受您的翻譯體驗！* 