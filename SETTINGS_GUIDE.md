# LLM 翻譯器設置指南

## 📋 概述

此翻譯器現在支援多種翻譯服務和完整的設置功能，讓您可以根據需求自訂翻譯體驗。

## 🔧 如何開啟設置

1. 運行 `LLM_Translator.exe`
2. 在系統托盤（右下角）找到翻譯器圖標
3. 右鍵點擊圖標
4. 選擇「設置」

## 🌐 翻譯服務設置

### Google翻譯（推薦）

**優點：**
- 免費使用（有每日限制）
- 高品質翻譯
- 支援多種語言
- 無需API密鑰

**設置步驟：**
1. 在「翻譯服務」標籤頁選擇「Google翻譯」
2. 選擇您的預設目標語言
3. 點擊「儲存」

**支援語言：**
- 繁體中文 (zh-TW)
- 簡體中文 (zh-CN)
- 英文 (en)
- 日文 (ja)
- 韓文 (ko)
- 法文 (fr)
- 德文 (de)
- 西班牙文 (es)

### Google翻譯 API（專業版）

如果您需要更高的使用限制，可以使用Google翻譯API：

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 啟用 Cloud Translation API
3. 建立API密鑰
4. 在設置中填入API密鑰

## 🤖 自定義LLM設置

### 支援的LLM服務

任何支援OpenAI格式API的服務都可以使用：

- **OpenAI ChatGPT**
  - API URL: `https://api.openai.com/v1/chat/completions`
  - 需要OpenAI API密鑰

- **Claude (Anthropic)**
  - 需要適配器或相容API

- **本地LLM服務**
  - Ollama
  - LocalAI
  - 其他本地部署的模型

### 設置步驟

1. 在「自定義LLM」標籤頁中：
   - ✅ 勾選「啟用自定義LLM」
   - 填入「API URL」
   - 填入「API密鑰」（如果需要）
   - 自訂「系統提示詞」

2. 在「翻譯服務」標籤頁選擇「自定義LLM」

### 系統提示詞範例

**預設提示詞：**
```
You are a professional translator. Translate the following text accurately while preserving the original meaning and context. Only provide the translation without any additional explanation.
```

**自訂繁體中文提示詞：**
```
你是一位專業的翻譯師。請將以下文字準確翻譯成繁體中文，保持原文的意思和語境。只提供翻譯結果，不要包含任何額外說明。
```

**商業文件翻譯：**
```
You are a professional business translator. Translate the following text into Traditional Chinese, maintaining formal tone and business terminology. Preserve original formatting and only provide the translation.
```

**技術文件翻譯：**
```
You are a technical translator specializing in software and technology. Translate the following text accurately while preserving technical terms and code snippets. Output only the translation in Traditional Chinese.
```

## ⚙️ 一般設置

### 翻譯行為
- **自動翻譯**：啟用後會自動翻譯複製的文字
- **保持原文格式**：保持原文的段落和格式

### 介面設置
- **字體大小**：調整翻譯視窗的字體大小（10-20px）
- **視窗透明度**：調整翻譯視窗的透明度（70%-100%）

## 🚀 使用方法

1. **基本翻譯**：
   - 選取任意文字
   - 按 `Ctrl+C` 複製
   - 翻譯視窗會自動彈出

2. **複製翻譯結果**：
   - 在翻譯視窗中點擊「複製」按鈕
   - 或使用快捷鍵 `Ctrl+Shift+C`

3. **關閉翻譯視窗**：
   - 點擊「關閉」按鈕
   - 或點擊視窗外的任意位置

## 🔧 疑難排解

### Google翻譯無法使用
- 檢查網路連線
- 確認未超過每日使用限制
- 如使用API，檢查API密鑰是否正確

### 自定義LLM無回應
- 檢查API URL是否正確
- 確認API密鑰有效
- 檢查LLM服務是否運行中
- 確認API格式與OpenAI相容

### 翻譯視窗不出現
- 檢查是否有選取文字
- 確認已按Ctrl+C複製
- 檢查託盤圖標是否顯示

### 效能問題
- 使用Google翻譯獲得最快速度
- 本地LLM可能較慢但更私密
- 調整視窗透明度可改善效能

## 📝 配置檔案位置

設置會自動儲存到 `config.json` 檔案中。如需手動編輯：

```json
{
    "translation_service": {
        "provider": "google",
        "google_api": {
            "api_key": "",
            "endpoint": "https://translation.googleapis.com/language/translate/v2"
        },
        "custom_llm": {
            "enabled": false,
            "api_url": "",
            "api_key": "",
            "system_prompt": "..."
        }
    }
}
```

## 💡 使用建議

1. **日常使用**：建議使用Google翻譯，速度快且品質佳
2. **專業翻譯**：使用自定義LLM配合專業提示詞
3. **隱私考量**：使用本地LLM確保數據不外洩
4. **多語言需求**：設置不同的系統提示詞檔案

## 🆕 更新功能

- ✅ 支援Google翻譯和自定義LLM
- ✅ 完整的設置界面
- ✅ 多語言目標選擇
- ✅ 自定義系統提示詞
- ✅ 翻譯結果複製功能
- ✅ 錯誤處理和顯示
- ✅ 非同步翻譯避免界面凍結

需要協助？請參考 [README.md](README.md) 或提交issue。 