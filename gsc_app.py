import streamlit as st
import language_tool_python
from deep_translator import GoogleTranslator

# Initialize grammar tool
try:
    tool = language_tool_python.LanguageTool('en-US')
except Exception as e:
    st.error("⚠️ Failed to initialize grammar tool. Please check your internet or setup.")
    st.stop()

# Streamlit setup
st.set_page_config(page_title="Grammar & Spell Checker", layout="centered")
st.title("📝 Grammar & Spelling Auto Checker")
st.markdown("Enter or upload a sentence/paragraph to check grammar and translate:")

# --- File Upload ---
uploaded_file = st.file_uploader("📄 Upload a `.txt` file", type=["txt"])

if uploaded_file:
    text_input = uploaded_file.read().decode("utf-8")
    st.text_area("📘 Uploaded Text", value=text_input, height=200, key="file_text")
else:
    text_input = st.text_area("✍️ Manual Input", height=200, key="manual_text")

# --- Grammar Check ---
if st.button("✅ Check Grammar"):
    if not text_input.strip():
        st.warning("⚠️ Please enter or upload text.")
    else:
        try:
            matches = tool.check(text_input)
            corrected = language_tool_python.utils.correct(text_input, matches)

            st.subheader("✅ Corrected Text")
            st.success(corrected)

            st.subheader(f"🔍 Found {len(matches)} Issue(s)")
            if matches:
                for i, match in enumerate(matches, 1):
                    st.markdown(f"**{i}.** *{match.message}* — `{match.replacements}`")
            else:
                st.info("🎉 No grammar issues found!")
        except Exception as e:
            st.error(f"❌ Grammar check failed: {e}")

# --- Translation ---
st.divider()
st.subheader("🌐 Translate to another language")

languages = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr"
}

lang_display = st.selectbox("Select Language", list(languages.keys()))

if st.button("🌍 Translate"):
    if not text_input.strip():
        st.warning("⚠️ Please enter or upload text to translate.")
    else:
        try:
            lang_code = languages[lang_display]
            translated = GoogleTranslator(source='auto', target=lang_code).translate(text_input)
            st.success(f"**Translated to {lang_display}:**\n\n{translated}")
        except Exception as e:
            st.error(f"❌ Translation failed: {e}")
