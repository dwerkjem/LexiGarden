import os
import random

import nltk
from joblib import dump, load
from nltk.corpus import cmudict
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

nltk.download("cmudict")


def extractFeatures(word):
    d = cmudict.dict()
    syllables = (
        [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]]
        if word.lower() in d
        else [0]
    )
    return [
        len(word),
        sum(syllables) / len(syllables) if syllables else 0,
    ]


def getRandomWord():
    with open("data/data.csv", "r") as f:
        words = f.readlines()
    word = random.choice(words).strip()
    word, frequency = word.split(",")
    return word, int(frequency)


X = []  # Feature vectors
y = []  # Corresponding difficulties
model = None  # Initialize model variable

# Path where the model is saved
model_file_path = "data/ai.joblib"

# Check if a saved model exists and load it
if os.path.exists(model_file_path):
    model = load(model_file_path)
    print("Model loaded successfully.")
else:
    print("No saved model found. A new model will be trained.")

try:
    while True:
        word, frequency = getRandomWord()
        features = extractFeatures(word)
        print(f"Word: {word}, Features: {features}")

        # If model exists, predict the difficulty for the current word
        if model is not None:
            predicted_difficulty = model.predict([features + [frequency]])
            print(f"Predicted Difficulty (Before Training): {predicted_difficulty[0]}")

        difficulty = input("Difficulty (1-5 or 'exit' to stop): ")
        if difficulty.lower() == "exit":
            break
        else:
            difficulty = int(difficulty)
            assert 1 <= difficulty <= 5

        # Append new data point to training data
        X.append(features + [frequency])
        y.append(difficulty)

except AssertionError:
    print("Invalid difficulty level. Exiting...")

# Proceed with training or retraining the model as needed
if X and y:  # Ensure there is data to train on
    if model is None:  # If no model was loaded, initialize a new one
        model = RandomForestClassifier()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model.fit(X_train, y_train)  # Train or retrain the model

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy}")

    # Save or overwrite the model file
    dump(model, model_file_path)
    print(f"Model saved to {model_file_path}")
else:
    print("No data collected. Using existing model if available.")
