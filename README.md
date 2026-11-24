# 語音轉文字 → Word（Streamlit）

上傳 MP3 / WAV 等音檔，使用 OpenAI Whisper 轉成文字，並自動產生 Word 檔下載。

## 功能
- 支援多種音檔格式
- 可選擇 Whisper 模型大小與語言
- 一鍵產生並下載 .docx

## 本地執行
```bash
pip install -r requirements.txt
streamlit run app.py
