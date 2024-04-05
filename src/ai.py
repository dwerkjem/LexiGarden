import random

import numpy as np
from joblib import dump, load
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

import src.features


def extract_features(word):
    features = features.extractFeatures(word)
    return features


def getRandomWord():
    data = "data/data.csv"
    with open(data, "r") as f:
        lines = f.readlines()
        random_line = random.choice(lines)
        word = random_line.split(",")[0]
        return word


def loadModel():
    try:
        model = load("data/model.joblib")
    except FileNotFoundError:
        model = None
    return model


def saveModel(model):
    dump(model, "data/model.joblib")
    print("Model saved to data/model.joblib")


def saveRating(word, rating):
    filename = "data/ratings.txt"
    try:
        rating = int(rating)
        assert 1 <= rating <= 5
    except ValueError:
        print("Rating must be an integer exiting..")
        exit(1)
    # Initialize an empty dictionary to hold word ratings
    ratings_dict = {}

    try:
        with open(filename, "r") as f:
            for line in f:
                key, value = line.strip().split(",")
                # If the word already exists in the dictionary, append the new rating to its list
                # Otherwise, create a new list with the current rating
                if key in ratings_dict:
                    ratings_dict[key].append(value)
                else:
                    ratings_dict[key] = [value]
    except FileNotFoundError:
        print(f"No existing data file found. Creating a new one for {word}.")

    # Append the new rating for the word
    if word in ratings_dict:
        ratings_dict[word].append(rating)
    else:
        ratings_dict[word] = [rating]

    # Write the updated data back to the file
    with open(filename, "w") as f:
        for key, values in ratings_dict.items():
            for value in values:
                f.write(f"{key},{value}\n")

    print(f'Rating of {rating} appended to "{word}".')


def queryRating(word):
    filename = "data/ratings.txt"
    try:
        with open(filename, "r") as f:
            for line in f:
                key, value = line.strip().split(",")
                if key == word:
                    return value
    except FileNotFoundError:
        print(f"No existing data file found. Creating a new one for {word}.")
        return None


def dataModel():
    times = 0  # Number of times the model has been trained
    while True:
        print(f"Training model for the {times + 1}th time")
        word = getRandomWord()
        prev_rating = queryRating(word)
        if prev_rating is None:
            print(f"Rate the word: {word}")
            rating = input("Rating: ")
            saveRating(word, rating)
        else:
            print(f"Rating for {word} already exists: {prev_rating}")
            continue

        times += 1


def trainModel():
    pass


def testModel():
    pass


if __name__ == "__main__":
    print("Welcome to the AI module")
    choice = input("Enter 1 to train the model, 2 to rate words, 3 to test the model: ")
    if choice == "1":
        trainModel()
    elif choice == "2":
        dataModel()
    elif choice == "3":
        testModel()
    else:
        print("Invalid choice. Exiting...")
        exit(1)
