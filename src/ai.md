# AI Python File

## Table of Contents:

- [Overview](#overview)
- [How to Use](#how-to-use)
- [Line-by-Line Explanation](#line-by-line-explanation)
  - [Imports](#imports)
  - [Ensure nltk cmudict is downloaded](#ensure-nltk-cmudict-is-downloaded)
  - [Function to Extract Features](#function-to-extract-features)
  - [Function to Get Random Word](#function-to-get-random-word)
  - [Initialize Variables](#initialize-variables)
  - [Load or Train Model](#load-or-train-model)
  - [Main Loop](#main-loop)
  - [Train or Retrain Model](#train-or-retrain-model)

## Overview

This is the AI Python file. It is used to train a model that predicts the difficulty level of a word based on its features. The AI file uses the CMU Pronouncing Dictionary to extract features such as the number of syllables in a word. It then trains a Random Forest Classifier model on the extracted features and the difficulty levels provided by the user.

```python
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
```

## How to Use

1. Run `python3 ai.py` in the terminal only if you have the required dependencies installed (see readme.md).
2. The program will either load a saved model or train a new model.
3. For each word, the program will display the word and its features.
4. If a model is loaded, it will predict the difficulty level of the word.
5. Enter the difficulty level of the word (1-5) or type 'exit' to stop.
6. The program will collect the data and train the model accordingly.
7. The model will be saved to `data/ai.joblib` after training.
8. The program will display the model accuracy and exit.

## Line-by-Line Explanation

### Imports

```python
import os
import random

import nltk
from joblib import dump, load
from nltk.corpus import cmudict
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
```

the import statements import the required libraries and modules for the program.

- `os`: Provides a way to interact with the operating system.
- `random`: Provides functions for generating random numbers.
- `nltk`: Natural Language Toolkit library for natural language processing.
- `joblib`: Provides utilities for saving and loading Python objects.
- `cmudict`: CMU Pronouncing Dictionary from the NLTK corpus.
- `RandomForestClassifier`: A machine learning model for classification.
- `accuracy_score`: A function to calculate the accuracy of a model.
- `train_test_split`: A function to split data into training and testing sets.

### ensure nltk cmudict is downloaded

```python
nltk.download("cmudict")
```

This line downloads the CMU Pronouncing Dictionary from the NLTK corpus. The CMU Pronouncing Dictionary is used to extract features such as the number of syllables in a word.

### Function to Extract Features

```python
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
```

This function extracts features from a word. It uses the CMU Pronouncing Dictionary to get the number of syllables in the word. The features extracted are the length of the word and the average number of syllables per pronunciation.

### Function to Get Random Word

```python
def getRandomWord():
    with open("data/data.csv", "r") as f:
        words = f.readlines()
    word = random.choice(words).strip()
    word, frequency = word.split(",")
    return word, int(frequency)
```

This function reads a list of words and their frequencies from a CSV file and returns a random word along with its frequency.

### Initialize Variables

```python

X = []  # Feature vectors
y = []  # Corresponding difficulties
model = None  # Initialize model variable

```

These variables are used to store the feature vectors, corresponding difficulties, and the model. They are initialized to empty lists and `None`.

### Load or Train Model

```python
# Path where the model is saved
model_file_path = "data/ai.joblib"

# Check if a saved model exists and load it
if os.path.exists(model_file_path):
    model = load(model_file_path)
    print("Model loaded successfully.")
else:
    print("No saved model found. A new model will be trained.")
```

This code checks if a saved model exists in the specified file path. If a model is found, it is loaded using the `load` function from `joblib`. If no model is found, a message is displayed indicating that a new model will be trained.

### Main Loop

```python
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

```

This code runs a loop that collects data for training the model. It gets a random word and its features, displays the word and features, and prompts the user to enter the difficulty level of the word. If a model is loaded, it predicts the difficulty level before training. The loop continues until the user types `'exit'` or enters an invalid difficulty level.

### Train or Retrain Model

```python
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
```

This code checks if there is data collected for training. If there is data, it checks if a model is loaded. If no model is loaded, it initializes a new `RandomForestClassifier` model. It then splits the data into training and testing sets, trains or retrains the model, calculates the accuracy of the model, saves the model to the specified file path, and displays a message indicating the model has been saved.
