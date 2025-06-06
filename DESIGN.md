# LLM Translator Design Document

## Core Features

### 1. Translation Engine
- **Multiple LLM Support**
  - OpenAI GPT-4/3.5
  - Anthropic Claude
  - Local LLM options (optional)
- **Translation Modes**
  - Chinese to English
  - English to Traditional Chinese
  - Auto-detect language
  - Custom language pairs

### 2. User Interface
- **System Tray Integration**
  - Status indicator
  - Quick settings access
  - Translation history
  - Exit option

- **Translation Window**
  - Floating window with transparency
  - Auto-positioning near cursor
  - Drag-and-drop support
  - Resizable interface
  - Dark/Light theme support

- **Main Settings Window**
  - API configuration
  - Translation preferences
  - Hotkey customization
  - Theme settings
  - Language pair settings

### 3. Text Selection & Processing
- **Selection Methods**
  - Mouse selection (Ctrl+C)
  - Custom hotkey
  - Clipboard monitoring
  - Manual input

- **Text Processing**
  - Smart text cleaning
  - Format preservation
  - Special character handling
  - Code snippet support

### 4. Translation Features
- **Smart Translation**
  - Context-aware translation
  - Technical term handling
  - Domain-specific translation
  - Maintain formatting

- **Additional Features**
  - Translation history
  - Favorite translations
  - Export/Import settings
  - Batch translation

### 5. Performance & Optimization
- **Caching System**
  - Translation cache
  - API response cache
  - Settings cache

- **Resource Management**
  - Memory optimization
  - CPU usage optimization
  - Network request optimization

## Technical Implementation

### 1. Core Components
```python
class TranslationEngine:
    - API integration
    - Translation logic
    - Error handling
    - Rate limiting

class UIManager:
    - Window management
    - Theme handling
    - Event processing
    - Layout management

class TextProcessor:
    - Text cleaning
    - Format handling
    - Language detection
    - Special cases

class CacheManager:
    - Translation cache
    - Settings storage
    - History management
```

### 2. Data Flow
1. Text Selection → TextProcessor
2. TextProcessor → TranslationEngine
3. TranslationEngine → CacheManager
4. CacheManager → UIManager
5. UIManager → Display

### 3. Configuration System
```json
{
    "api": {
        "provider": "openai",
        "api_key": "encrypted_key",
        "model": "gpt-4"
    },
    "translation": {
        "default_source": "auto",
        "default_target": "zh-TW",
        "preserve_format": true
    },
    "ui": {
        "theme": "light",
        "window_opacity": 0.95,
        "font_size": 14
    },
    "hotkeys": {
        "translate": "ctrl+c",
        "settings": "ctrl+alt+s"
    }
}
```

## Usage Guide

### Basic Usage
1. **Installation**
   ```bash
   pip install -r requirements.txt
   python icon.py
   python translator.py
   ```

2. **First-time Setup**
   - Configure API keys in settings
   - Choose default language pair
   - Set preferred hotkeys
   - Select theme

3. **Daily Usage**
   - Select text (Ctrl+C)
   - View translation in popup
   - Use quick actions in popup
   - Access history from tray icon

### Advanced Features
1. **Custom Translation Rules**
   - Add domain-specific terms
   - Set preferred translations
   - Configure format preservation

2. **Batch Translation**
   - Select multiple texts
   - Use batch processing
   - Export results

3. **History Management**
   - View translation history
   - Search past translations
   - Export/Import history

### Keyboard Shortcuts
- `Ctrl+C`: Translate selected text
- `Ctrl+Alt+S`: Open settings
- `Ctrl+Alt+H`: Show history
- `Esc`: Close translation window
- `Ctrl+Shift+C`: Copy translation

## Error Handling
1. **API Errors**
   - Automatic retry
   - Fallback options
   - User notification

2. **Network Issues**
   - Offline mode
   - Queue system
   - Sync when online

3. **UI Issues**
   - Window recovery
   - State preservation
   - Error logging

## Performance Considerations
1. **Memory Usage**
   - Efficient caching
   - Resource cleanup
   - Memory monitoring

2. **Response Time**
   - Optimized API calls
   - Local processing
   - Background tasks

3. **Battery Impact**
   - Power-aware processing
   - Sleep mode handling
   - Resource throttling 