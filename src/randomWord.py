import random

import pandas as pd

path = "data/data.csv"


def randomWord():
    with open(path, "r") as f:
        lines = f.readlines()
        word = random.choice(lines)
        return word.split(",")[0]


def getRandomWordOfLength(length):
    df = pd.read_csv(path)
    # Find the row where the word matches
    word_row = df.loc[df["Length_of_First_Column"] == length]
    if not word_row.empty:
        # Display a random word of the given length
        return word_row.sample()
    else:
        return "Word not found."


if __name__ == "__main__":
    print(randomWord())
    print(getRandomWordOfLength(14))
