import random

path = "data/data.csv"


def randomWord():
    with open(path, "r") as f:
        lines = f.readlines()
        word = random.choice(lines)
        return word.split(",")[0]
