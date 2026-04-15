import streamlit as st

# 🔷 GLOBAL UI
def apply_ui():
    st.markdown("""
    <style>

    /* 🔥 REMOVE ALL DEFAULT PADDING (REAL FIX) */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: 0rem !important;
    }

    /* 🔥 REMOVE HEADER GAP (IMPORTANT) */
    header {
        visibility: hidden;
    }

    /* 🔥 FULL PAGE BACKGROUND */
    .stApp {
        background: linear-gradient(
            rgba(15, 23, 42, 0.92),
            rgba(15, 23, 42, 0.95)
        ),
        url("https://images.unsplash.com/photo-1518770660439-4636190af475");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* 🔥 MAIN CONTAINER FULL WIDTH */
    .main {
        padding-top: 0rem !important;
    }

    /* 🏷️ TITLE FIX (NOT CUT) */
    h1 {
        color: #60a5fa;
        text-align: center;
        font-weight: 800;
        margin-top: 20px !important;
        padding-top: 10px;
    }

    /* 🧾 SUBTITLE */
    p {
        text-align: center;
        color: #e2e8f0;
        font-weight: 600;
        margin-top: -5px;
    }

    /* 🔘 BUTTONS */
    div.stButton > button {
        background: linear-gradient(135deg, #2563eb, #1e40af);
        color: white;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.3);
        padding: 10px;
        font-size: 14px;
        font-weight: 700;
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.6);
    }

    /* 📊 SIDEBAR */
    section[data-testid="stSidebar"] {
        background: rgba(2, 6, 23, 0.95);
    }

    section[data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }

    </style>
    """, unsafe_allow_html=True)


# 🔷 BUTTONS (ALIGNED)
def show_buttons(col):
    b1, b2, b3, b4 = col.columns(4)

    with b1:
        add_letter = st.button("Add Letter", use_container_width=True)

    with b2:
        add_word = st.button("Add Word", use_container_width=True)

    with b3:
        space = st.button("Space", use_container_width=True)

    with b4:
        clear = st.button("Clear", use_container_width=True)

    return add_letter, add_word, space, clear


# 🔷 WORD BUILDER (SAFE)
def show_word_builder(col, word):
    col.subheader("Word Builder")
    col.write(word if word else "-")


# 🔷 SENTENCE BUILDER (SAFE - NO HTML BUG)
def show_sentence_builder(col, sentence, translated):
    col.subheader("Sentence Builder")

    col.write("Original:")
    col.write(sentence if sentence else "-")

    col.write("Translated:")
    col.write(translated if translated else "-")


# 🔷 PREDICTION (CLEAN STYLE)
def show_prediction(container, prediction, confidence):
    container.markdown(f"""
    ### 🔵 {prediction}
    Confidence: {confidence:.2f}
    """)
