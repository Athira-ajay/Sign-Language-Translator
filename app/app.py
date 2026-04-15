import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from gtts import gTTS
import tempfile
from googletrans import Translator
from ui_design import apply_ui, show_word_builder, show_sentence_builder, show_prediction, show_buttons

st.set_page_config(page_title="Sign Language Translator", layout="wide")
apply_ui()

st.title("🤟 SIGN LANGUAGE TRANSLATOR")
st.markdown("Real-Time Gesture Recognition using Deep Learning")

# Load model
model = tf.keras.models.load_model(
    "models/sign_language_model.h5",
    compile=False
)

labels = np.load("data/label_names.npy", allow_pickle=True)

# Translator (SAFE)
translator = Translator()

def translate_text(text, dest_lang):
    try:
        translated = translator.translate(text, dest=dest_lang)
        return translated.text
    except:
        return text  # fallback (no crash)

# Mediapipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7
)

# ---------------- SESSION STATE ----------------
if "current_prediction" not in st.session_state:
    st.session_state.current_prediction = ""

if "word" not in st.session_state:
    st.session_state.word = ""

if "sentence" not in st.session_state:
    st.session_state.sentence = ""

# ---------------- LANGUAGE SELECTION ----------------
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

frame_window = col1.image([])

# ✅ SINGLE prediction placeholder (TOP)
prediction_placeholder = col2.empty()

# ---------------- BUTTONS (ALIGNED) ----------------
add_letter, add_word, space, clear = show_buttons(col2)

if add_letter:
    if st.session_state.current_prediction != "":
        st.session_state.word += st.session_state.current_prediction

if add_word:
    if st.session_state.word != "":
        # ✅ FIXED (no disappearing bug)
        
        # Add space only if needed
        if st.session_state.sentence != "" and not st.session_state.sentence.endswith(" "):
            st.session_state.sentence += " "
            
        st.session_state.sentence += st.session_state.word + " "
        st.session_state.word = ""

if space:
    if not st.session_state.sentence.endswith(" "):
        st.session_state.sentence += " "
        
if clear:
    st.session_state.word = ""
    st.session_state.sentence = ""

# ---------------- DISPLAY ----------------
show_word_builder(col2, st.session_state.word)

# Translation
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
    if st.session_state.sentence.strip() != "":
        tts = gTTS(
            text=translated_sentence,
            lang=lang_code[language]
        )

        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp_file.name)

        audio_file = open(tmp_file.name, "rb")
        audio_bytes = audio_file.read()

        st.audio(audio_bytes)

# ---------------- CAMERA ----------------
run = st.sidebar.checkbox("Start Camera")

cap = cv2.VideoCapture(0)

prediction_buffer = []

while run:

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    landmarks = []

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            for lm in hand_landmarks.landmark:
                landmarks.append(lm.x)
                landmarks.append(lm.y)

    # Pad for 2 hands
    while len(landmarks) < 84:
        landmarks.append(0)

    if len(landmarks) >= 42:

        data = np.array(landmarks[:42]).reshape(1, -1)

        prediction = model.predict(data, verbose=0)

        class_id = np.argmax(prediction)
        confidence = np.max(prediction)

        gesture = labels[class_id]

        prediction_buffer.append(gesture)

        if len(prediction_buffer) > 10:
            prediction_buffer.pop(0)

        final_prediction = max(set(prediction_buffer), key=prediction_buffer.count)

        # Store prediction
        st.session_state.current_prediction = final_prediction

        # ✅ SINGLE prediction update (NO MULTIPLE CARDS)
        show_prediction(prediction_placeholder, final_prediction, confidence)

    frame_window.image(frame, channels="BGR")

cap.release()
