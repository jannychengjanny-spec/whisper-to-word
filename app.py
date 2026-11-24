import streamlit as st
import whisper
from docx import Document
import tempfile
import os
from io import BytesIO

# 頁面設定
st.set_page_config(
    page_title="語音轉文字 → Word",
    page_icon="🎤",
    layout="centered"
)

st.title("🎤 語音轉文字 → Word 文件")
st.markdown("上傳 MP3 / WAV / M4A 音檔，自動轉成文字並產生 Word 檔下載。")

# 側邊欄設定
with st.sidebar:
    st.header("設定")
    model_size = st.selectbox(
        "Whisper 模型大小",
        options=["tiny", "base", "small"],
        index=1,
        help="模型越大準確度越高，但執行越慢、記憶體需求越大。建議先用 base。"
    )
    language = st.selectbox(
        "語言",
        options=["zh", "en", "ja", "ko", "auto"],
        index=0,
        help="選擇 zh 可提高中文辨識準確度；選 auto 則自動偵測。"
    )
    st.markdown("---")
    st.markdown("**使用說明**")
    st.markdown("1. 上傳音檔\n2. 點擊「開始轉換」\n3. 等待完成後下載 Word")

# 上傳音檔
uploaded_file = st.file_uploader(
    "請上傳音檔（支援 mp3、wav、m4a、ogg）",
    type=["mp3", "wav", "m4a", "ogg", "flac"]
)

if uploaded_file is not None:
    st.audio(uploaded_file, format=f"audio/{uploaded_file.type.split('/')[-1]}")

    if st.button("🚀 開始轉換", type="primary", use_container_width=True):
        with st.spinner("正在載入模型並轉換中，請稍候（第一次會比較久）..."):
            try:
                # 將上傳檔案寫入暫存
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name

                # 載入 Whisper 模型
                model = whisper.load_model(model_size)

                # 轉文字
                if language == "auto":
                    result = model.transcribe(tmp_path)
                else:
                    result = model.transcribe(tmp_path, language=language)

                transcribed_text = result["text"].strip()

                # 清理暫存檔
                os.unlink(tmp_path)

                if not transcribed_text:
                    st.error("未能辨識出文字，請確認音檔是否清晰。")
                else:
                    st.success("轉換完成！")
                    st.subheader("轉換結果預覽")
                    st.text_area("文字內容", transcribed_text, height=250)

                    # 產生 Word 檔
                    doc = Document()
                    doc.add_heading("語音轉文字結果", level=1)
                    doc.add_paragraph(transcribed_text)

                    # 把 Word 存到記憶體
                    buffer = BytesIO()
                    doc.save(buffer)
                    buffer.seek(0)

                    # 下載按鈕
                    st.download_button(
                        label="📥 下載 Word 檔案",
                        data=buffer,
                        file_name="語音轉文字結果.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )

            except Exception as e:
                st.error(f"發生錯誤：{str(e)}")
                st.info("若出現記憶體不足，請改選較小的模型（tiny 或 base）。")
else:
    st.info("請先上傳音檔。")
