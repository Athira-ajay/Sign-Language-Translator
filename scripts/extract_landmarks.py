import os
import cv2
import mediapipe as mp
import pandas as pd

# Paths
DATASET_PATH = "datasets/final_dataset"
CSV_PATH = "datasets/landmark_dataset.csv"

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)

data = []
processed_labels = set()

# Resume support
if os.path.exists(CSV_PATH):
    print("Existing CSV found. Resuming extraction...")
    existing_df = pd.read_csv(CSV_PATH)
    processed_labels = set(existing_df.iloc[:, -1].unique())
    data = existing_df.values.tolist()

for label in os.listdir(DATASET_PATH):

    if label in processed_labels:
        print(f"Skipping {label} (already processed)")
        continue

    print(f"Processing: {label}")

    label_path = os.path.join(DATASET_PATH, label)

    for img_name in os.listdir(label_path):

        img_path = os.path.join(label_path, img_name)
        img = cv2.imread(img_path)

        if img is None:
            continue

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(img_rgb)

        if result.multi_hand_landmarks:

            landmarks = []

            for lm in result.multi_hand_landmarks[0].landmark:
                landmarks.append(lm.x)
                landmarks.append(lm.y)

            landmarks.append(label)
            data.append(landmarks)

    # Save after each label (checkpoint)
    df = pd.DataFrame(data)
    df.to_csv(CSV_PATH, index=False)

    print(f"{label} saved")

print("Landmark extraction completed!")