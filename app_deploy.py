import streamlit as st
import numpy as np
from gtts import gTTS
import tempfile
from googletrans import Translator

from ui_design import apply_ui, show_word_builder, show_sentence_builder, show_prediction, show_buttons

st.set_page_config(page_title="Sign Language Translator", layout="wide")
apply_ui()

st.title("🤟 SIGN LANGUAGE TRANSLATOR")
st.markdown("Real-Time Gesture Recognition using Deep Learning")

# ---------------- SESSION STATE ----------------
if "current_prediction" not in st.session_state:
    st.session_state.current_prediction = "A"

if "word" not in st.session_state:
    st.session_state.word = ""

if "sentence" not in st.session_state:
    st.session_state.sentence = ""

translator = Translator()

def translate_text(text, dest_lang):
    try:
        return translator.translate(text, dest=dest_lang).text
    except:
        return text

# ---------------- SIDEBAR ----------------
st.sidebar.subheader("🌍 Language Settings")

language = st.sidebar.selectbox(
    "Select Language",
    ["English", "Hindi", "Malayalam"]
)

lang_code = {
    "English": "en",
    "Hindi": "hi",
    "Malayalam": "ml"
}

# ---------------- LAYOUT ----------------
col1, col2 = st.columns([2,1])

# ---------------- PREDICTION CARD ----------------
prediction_placeholder = col2.empty()
show_prediction(prediction_placeholder, st.session_state.current_prediction, 0.95)

# ---------------- BUTTONS ----------------
add_letter, add_word, clear = show_buttons(col2)

if add_letter:
    st.session_state.word += st.session_state.current_prediction

if add_word:
    if st.session_state.word:
        st.session_state.sentence += st.session_state.word + " "
        st.session_state.word = ""

if clear:
    st.session_state.word = ""
    st.session_state.sentence = ""

# ---------------- DISPLAY ----------------
show_word_builder(col2, st.session_state.word)

translated_sentence = translate_text(
    st.session_state.sentence,
    lang_code[language]
)

show_sentence_builder(
    col2,
    st.session_state.sentence,
    translated_sentence
)

# ---------------- SPEECH ----------------
if col2.button("🔊 Speak Sentence"):
    if st.session_state.sentence.strip():
        tts = gTTS(text=translated_sentence, lang=lang_code[language])
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp.name)
        audio = open(tmp.name, "rb").read()
        st.audio(audio)

st.info("📌 Live gesture detection works in local version (camera not supported in cloud).")