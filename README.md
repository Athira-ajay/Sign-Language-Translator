🤟 SIGN LANGUAGE TRANSLATOR

A real-time Sign Language Translator web application that detects hand gestures using computer vision and deep learning, and converts them into text, speech, and regional languages.

Features

- 🔴 Real-time hand gesture recognition using webcam
- ✍️ Word Builder (create words from detected gestures)
- 💬 Sentence Builder (form full sentences)
- 🌍 Multi-language translation (English, Hindi, Malayalam)
- 🔊 Text-to-Speech (voice output with accent)
- 🎨 Clean and modern UI using Streamlit

Technologies Used

- Python
- Streamlit
- OpenCV
- MediaPipe
- TensorFlow / Keras
- gTTS (Text-to-Speech)
- Googletrans (Translation)

Project Structure

Sign-Language-Translator/
│── app.py
│── ui_design.py
│── requirements.txt
│── models/
│ └── sign_language_model.h5
│── data/
│ └── label_names.npy

How to Run Locally

git clone https://github.com/Athira-ajay/Sign-Language-Translator
cd Sign-Language-Translator

pip install -r requirements.txt

streamlit run app.py

Future Improvements

  - Add more gesture classes
  - Improve model accuracy
  - Add user authentication (login system)
  - Deploy mobile-friendly version
  - Save translated text history

Author

Athira Ajay
B.Tech Computer Science Student
