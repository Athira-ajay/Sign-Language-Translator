import cv2
import os
import numpy as np
import mediapipe as mp

# Path to dataset
DATASET_PATH = "datasets/final_dataset"

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True)

# Lists to store data
landmarks = []
labels = []
label_names = []

# Get gesture folder names
for label in os.listdir(DATASET_PATH):

    folder_path = os.path.join(DATASET_PATH, label)

    if os.path.isdir(folder_path):
        label_names.append(label)

print("Found gesture labels:")
print(label_names)
print("Total gesture folders:", len(label_names))


# Loop through each gesture folder
for label_index, label in enumerate(label_names):

    folder_path = os.path.join(DATASET_PATH, label)

    # LIMIT number of images per folder
    image_files = os.listdir(folder_path)[:300]

    print("\nProcessing gesture:", label)
    print("Total images used:", len(image_files))

    for i, image_name in enumerate(image_files):

        # Print progress every 100 images
        if i % 100 == 0:
            print("Processed", i, "images...")

        image_path = os.path.join(folder_path, image_name)

        image = cv2.imread(image_path)

        if image is None:
            continue

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:

            hand_landmarks = []

            for lm in results.multi_hand_landmarks[0].landmark:
                hand_landmarks.append(lm.x)
                hand_landmarks.append(lm.y)

            landmarks.append(hand_landmarks)
            labels.append(label_index)

print("\nTotal samples collected:", len(landmarks))

# Create data folder
os.makedirs("data", exist_ok=True)

# Save dataset
np.save("data/landmarks.npy", np.array(landmarks))
np.save("data/labels.npy", np.array(labels))
np.save("data/label_names.npy", np.array(label_names))

print("\nDataset built successfully!")