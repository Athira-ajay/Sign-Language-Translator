import numpy as np
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

# Load dataset
X = np.load("data/landmarks.npy")
y = np.load("data/labels.npy")
label_names = np.load("data/label_names.npy", allow_pickle=True)

print("Dataset loaded")
print("Samples:", X.shape)
print("Labels:", y.shape)
print("Classes:", len(label_names))

# Convert labels to categorical
y = to_categorical(y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Training samples:", X_train.shape)
print("Testing samples:", X_test.shape)

# Build Neural Network model
model = Sequential()

model.add(Dense(128, activation="relu", input_shape=(42,)))
model.add(Dense(64, activation="relu"))
model.add(Dense(32, activation="relu"))
model.add(Dense(len(label_names), activation="softmax"))

# Compile model
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

print("\nStarting training...\n")

# Train model
history = model.fit(
    X_train,
    y_train,
    epochs=30,
    batch_size=32,
    validation_data=(X_test, y_test)
)

# Create models folder if not exists
os.makedirs("models", exist_ok=True)

# Save trained model
model.save("models/sign_language_model.h5")

print("\nModel training completed!")
print("Model saved in models/sign_language_model.h5")