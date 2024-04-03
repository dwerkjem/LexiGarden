import nltk

nltk.download("words")
from nltk.corpus import words

word_list = set(words.words())  # Load the word list from nltk


def first_word_in_dictionary_and_unique(line, encountered_words):
    words_in_line = (
        line.strip().split()
    )  # Strip leading/trailing whitespace and split the line into words
    if not words_in_line:  # If the list is empty, return False immediately
        return False
    first_word = words_in_line[
        0
    ].lower()  # Convert to lowercase to match the word list format
    if first_word in encountered_words:
        return False  # Skip duplicate
    if first_word in word_list:
        encountered_words.add(
            first_word
        )  # Add to encountered words to track duplicates
        return True
    return False


# Path to the input file
input_file_path = "processed_combined.txt"
# Path to the output file
output_file_path = "final.txt"

encountered_words = set()  # Initialize an empty set to track encountered first words

# Open the input file and process it line by line
with open(input_file_path, "r") as input_file, open(
    output_file_path, "w"
) as output_file:
    for line in input_file:
        # Check if the first word is in the dictionary and not a duplicate
        if first_word_in_dictionary_and_unique(line, encountered_words):
            # If so, write the line to the output file
            output_file.write(
                line.lower()
            )  # Convert the entire line to lowercase before writing

print(
    "File has been processed, duplicates removed, converted to lowercase, and output saved to:",
    output_file_path,
)
