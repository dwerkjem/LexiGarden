import nltk
from nltk.corpus import cmudict

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")


nltk.download("cmudict", quiet=True)

consonants = "bcdfghjklmnpqrstvwxyz"
vowels = "aeiou"


def count_syllables(word):
    word = word.lower()
    vowels = "aeiou"
    count = 0
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count = 1
    return count


def frequency(word):
    with open("data/data.csv", "r") as f:
        words = f.readlines()
    for w in words:
        if w.split(",")[0] == word:
            return int(w.split(",")[1])
    return 0


def extractFeatures(word):
    features = {}
    features["length"] = len(word)
    features["num_syllables"] = len(
        cmudict.dict().get(word.lower(), [])
    ) or count_syllables(word)
    features["num_vowels"] = len([c for c in word.lower() if c in vowels])
    features["num_consonants"] = len([c for c in word.lower() if c in consonants])
    features["percent_vowels"] = (
        features["num_vowels"] / features["length"] if features["length"] > 0 else 0
    )
    features["percent_consonants"] = (
        features["num_consonants"] / features["length"] if features["length"] > 0 else 0
    )
    features["avreage_syllables"] = (
        features["num_syllables"] / features["length"] if features["length"] > 0 else 0
    )
    features["num_vowels_per_syllable"] = (
        features["num_vowels"] / features["num_syllables"]
        if features["num_syllables"] > 0
        else 0
    )
    features["num_consonants_per_syllable"] = (
        features["num_consonants"] / features["num_syllables"]
        if features["num_syllables"] > 0
        else 0
    )
    features["num_vowels_per_consonant"] = (
        features["num_vowels"] / features["num_consonants"]
        if features["num_consonants"] > 0
        else 0
    )

    # POS tagging
    pos = nltk.pos_tag(nltk.word_tokenize(word))
    pos_counts = {}
    for tag in pos:
        pos_counts[tag[1]] = pos_counts.get(tag[1], 0) + 1
    total_tags = sum(pos_counts.values())
    for tag in pos_counts:
        features["pos_" + tag] = pos_counts[tag] / total_tags if total_tags > 0 else 0

    features["frequency"] = frequency(word)

    return features


if __name__ == "__main__":
    word = input("Enter a word: ")
    features = extractFeatures(word)
    print(features)
