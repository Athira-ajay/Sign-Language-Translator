import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf

# ------------------- LOAD MODEL -------------------
model = tf.keras.models.load_model(
    "models/sign_language_model.h5",
    compile=False
)

labels = np.load("data/label_names.npy", allow_pickle=True)

# ------------------- MEDIAPIPE -------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7
)

# ------------------- CAMERA -------------------
cap = cv2.VideoCapture(0)

print("Press Q to exit")

prediction_buffer = []

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    landmarks = []

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            # Draw landmarks
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            for lm in hand_landmarks.landmark:
                landmarks.append(lm.x)
                landmarks.append(lm.y)

    # ------------------- PREDICTION -------------------
    if len(landmarks) == 42:

        data = np.array(landmarks).reshape(1, -1)

        prediction = model.predict(data, verbose=0)

        class_id = np.argmax(prediction)
        confidence = np.max(prediction)

        gesture = labels[class_id]

        # Smooth prediction
        prediction_buffer.append(gesture)

        if len(prediction_buffer) > 10:
            prediction_buffer.pop(0)

        final_prediction = max(set(prediction_buffer), key=prediction_buffer.count)

        # Display prediction
        cv2.putText(
            frame,
            f"{final_prediction} ({confidence:.2f})",
            (50, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 255, 0),
            3
        )

    # ------------------- SHOW WINDOW -------------------
    cv2.imshow("Sign Language Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()