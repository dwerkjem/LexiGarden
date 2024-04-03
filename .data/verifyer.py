import csv

import nltk
from nltk.corpus import words
from tqdm import tqdm


def is_real_word(word, word_set):
    # Assuming the format "word,number", split and take the word part
    word_only = word.split(",")[0].lower()
    return word_only in word_set


def process_csv(input_file, output_file):
    word_set = set(words.words())

    try:
        with open(input_file, "r") as csvfile, open(
            output_file, "w", newline=""
        ) as output_csvfile:
            reader = csv.reader(csvfile)
            writer = csv.writer(output_csvfile)

            pbar = tqdm(desc="Processing", unit="row")
            words_not_found = []  # For diagnostic purposes

            for row in reader:
                word = row[0].strip('"')  # Adjust this index as necessary
                if is_real_word(word, word_set):
                    writer.writerow(row)
                else:
                    words_not_found.append(
                        word
                    )  # Collect words not found for diagnostic
                pbar.update(1)

            pbar.close()

            # Diagnostic: print or log words not found
            print(
                f"Words not found in NLTK corpus: {words_not_found[:10]}"
            )  # Print first 10 for review

    except IOError as e:
        print(f"An error occurred while processing files: {e}")


if __name__ == "__main__":
    input_file = "data.csv"  # Adjust as necessary
    output_file = "filtered_data.csv"  # Adjust as necessary

    process_csv(input_file, output_file)
    print("Processing completed. Filtered data is saved in", output_file)
