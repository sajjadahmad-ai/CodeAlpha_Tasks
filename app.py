import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import io
import streamlit.components.v1 as components

# ---- Page Setup ----
st.set_page_config(page_title="Language Translation Tool", page_icon="🌐")
st.title("🌐 Language Translation Tool")
st.write("Write Text, Select language, and get translation!")

# ---- Supported Languages ----
languages = GoogleTranslator().get_supported_languages(as_dict=True)
# languages is a dict like {'english': 'en', 'hindi': 'hi', ...}

lang_names = list(languages.keys())

# ---- User Input ----
input_text = st.text_area("Wite your text here :", height=150)

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("Source Language:", ["auto"] + lang_names)
with col2:
    target_lang = st.selectbox("Target Language:", lang_names, index=lang_names.index("english"))

# ---- Translate Button ----
if st.button("Translate 🔄"):
    if input_text.strip() == "":
        st.warning("Write text first!")
    else:
        try:
            src_code = "auto" if source_lang == "auto" else languages[source_lang]
            tgt_code = languages[target_lang]

            translated = GoogleTranslator(source=src_code, target=tgt_code).translate(input_text)

            st.success("Translation Complete!")
            st.text_area("Translated Text:", value=translated, height=150)

            # ---- Copy Button ----
            copy_html = f"""
                <textarea id="copyText" style="position:absolute; left:-9999px;">{translated}</textarea>
                <button onclick="navigator.clipboard.writeText(document.getElementById('copyText').value)"
                    style="padding:8px 16px; border-radius:6px; border:none; background-color:#4CAF50; color:white; cursor:pointer;">
                    📋 Copy Text
                </button>
            """
            components.html(copy_html, height=50)

            # ---- Text-to-Speech ----
            if st.button("🔊 Listen to Translation"):
                try:
                    tts = gTTS(text=translated, lang=tgt_code)
                    audio_bytes = io.BytesIO()
                    tts.write_to_fp(audio_bytes)
                    audio_bytes.seek(0)
                    st.audio(audio_bytes, format="audio/mp3")
                except Exception as tts_error:
                    st.warning(f"Awaaz nahi ban saki (shayad yeh language TTS support nahi karti): {tts_error}")

        except Exception as e:
            st.error(f"Error aayi: {e}")