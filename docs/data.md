# Data Set And Reproduction Information

## Table of Contents:

1. [Data Set Information](#data-set-information)
2. [Cleaning the Data](#cleaning-the-data)
3. [Reproducing the Data](#reproducing-the-data)
4. [Summary](#summary)

## Data Set Information:

This data set contains information about words in the English language. The data set contains the following columns:

1. `word`: The word in the English language.
2. `frequency`: The frequency of the word in the English language. According to the google books Ngram Viewer.

## Cleaning the Data:

The data is too large and contains many words that are not in the English language. We will filter the data to only include words that are in the English language and we only care about words that have appeared since 1900. We assume that all words that have appeared before 1900 are not relevant to the current English language. We will also remove any duplicates in the data set. We assume that all words that start with a letter. The data set contains multiple entries for the same word with different frequencies. We will add the frequencies of the same word together to get a single frequency for each word.

## Reproducing the Data:

pre-requisites:

- You need to have `curl` installed on your machine.
- Internet connection to download the data.
- at least 50GB of free space on your machine.
- Linux operating system. The scripts are written in bash and rust. The bash script will not work on windows. The rust script will work on MacOs but the requirements are not tested on MacOs. The scripts are tested on Arch Linux
- You need to have `python3` installed on your machine.

once you have the pre-requisites, you can follow the steps below to reproduce the data.

Steps to reproduce the data:

1. we will use a bash script to download the data from the google books Ngram Viewer. The script will download the data for each letter of the alphabet and save it in a directory called `ngram`. The script will also unzip the files after downloading them. A assumption is made that the script is run in a directory that is for the data and has at least 50GB of free space. To run the script, you can use the following code `./ngramDownloader.sh` in the terminal.

```bash
#!/bin/bash

# Define the base URL for the 1-gram files
base_url="http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-1gram-20120701-{letter}.gz"

# Create the ngram directory if it doesn't exist
mkdir -p ngram

# Loop through all letters of the alphabet
for letter in {a..z}; do
    # Replace {letter} in the URL with the current letter from the loop
    url="${base_url/\{letter\}/$letter}"

    # Define the filename for the downloaded file
    filename="ngram/${letter}.gz"

    # Use curl to download the file
    echo "Downloading ${url} into ${filename}..."
    curl -o "${filename}" "${url}"
    gunzip "${filename}"
done

echo "All downloads completed."
```

2. We will use a rust script to get rid of the data before 1900. The script will read each file in the `ngram` directory (relative to the current directory) and filter out any lines that contain a year before 1900. The script will then overwrite the files with the filtered data. The script will output any errors that occur during the process. To run the script, you can use the following code `./wordCompresser` in the terminal.

```rust
use std::fs::{self, File};
use std::io::{self, BufRead, BufReader, Write};
use std::path::Path;

fn compress(folder: &Path) -> io::Result<()> {
    // Iterate over files in the specified folder
    for entry in fs::read_dir(folder)? {
        let entry = entry?;
        let path = entry.path();

        // Skip directories
        if path.is_dir() {
            continue;
        }

        let file = File::open(&path)?;
        let reader = BufReader::new(file);
        let mut lines_to_write = Vec::new();

        for line in reader.lines() {
            let line = line?;
            // Split the line by whitespace and collect into a vector
            let parts: Vec<&str> = line.split_whitespace().collect();
            // Check if there's at least 2 parts and the second part is a year
            if parts.len() > 1 {
                if let Ok(year) = parts[1].parse::<i32>() {
                    // If the year is >= 1970, keep the line
                    if year >= 1900 {
                        lines_to_write.push(line);
                    }
                }
            } else {
                // If there's no year, keep the line as is
                lines_to_write.push(line);
            }
        }

        // Rewrite the file with the filtered and modified lines
        let mut file = File::create(&path)?;
        for line in lines_to_write {
            writeln!(file, "{}", line)?;
        }
    }
    Ok(())
}

fn main() {
    let folder = Path::new("ngram"); // Replace with your folder path
    if let Err(e) = compress(folder) {
        eprintln!("Error compressing files: {}", e);
    }
}
```

3. We will use a rust script to add the two frequencies of the same word together and aggregate all the years into one data point. The script will read each file in the `ngram` directory (relative to the current directory) for each letter of the alphabet and add the frequencies of the same word together. The script will then overwrite the files with the added frequencies. We do this because the data set contains multiple entries for the same word with different frequencies. To run the script, you can use the following code `./wordCompresser2` in the terminal.

```rust
use std::collections::HashMap;
use std::fs::{self, File};
use std::io::{self, BufRead, BufReader, Write};
use std::path::Path;

fn compress_and_aggregate(folder: &Path) -> io::Result<()> {
    for entry in fs::read_dir(folder)? {
        let entry = entry?;
        let path = entry.path();

        if path.is_dir() {
            continue;
        }

        let file = File::open(&path)?;
        let reader = BufReader::new(file);
        let mut word_counts = HashMap::new();

        for line in reader.lines() {
            let line = line?;
            // Assuming there can be multiple whitespace characters as separators
            let parts: Vec<&str> = line.split_whitespace().collect();
            if parts.len() == 4 {
                // Change the parsing to i64
                if let (Ok(n), Ok(n2)) = (parts[2].parse::<i64>(), parts[3].parse::<i64>()) {
                    *word_counts.entry(parts[0].to_string()).or_insert(0) += n + n2;
                }
            }
        }

        let mut file = File::create(&path)?;
        for (word, count) in word_counts {
            writeln!(file, "{} {}", word, count)?;
        }
    }
    Ok(())
}

fn main() {
    let folder = Path::new("ngram");
    if let Err(e) = compress_and_aggregate(folder) {
        eprintln!("Error processing files: {}", e);
    }
}
```

4. We will use a rust script to add all the files together. The script will read each file in the `ngram` directory (relative to the current directory) for each letter of the alphabet and add all the files together. The script will produce a single file called `combined.txt` that contains all the data from the individual files. To run the script, you can use the following code `./wordCompresser3` in the terminal.

```rust
use std::fs::{self, File, OpenOptions};
use std::io::{self, BufRead, BufReader, Write};
use std::path::Path;

fn append_files(folder: &Path, output_file_name: &str) -> io::Result<()> {
    let output_path = folder.join(output_file_name);
    let mut output_file = OpenOptions::new()
        .create(true)
        .write(true)
        .append(true)
        .open(&output_path)?;

    for entry in fs::read_dir(folder)? {
        let entry = entry?;
        let path = entry.path();

        // Skip if it is a directory or the output file itself
        if path.is_dir() || path.file_name() == Some(output_file_name.as_ref()) {
            continue;
        }

        let file = File::open(&path)?;
        let reader = BufReader::new(file);

        for line in reader.lines() {
            let line = line?;
            writeln!(output_file, "{}", line)?;
        }
    }
    Ok(())
}

fn main() {
    let folder_path = Path::new("ngram");
    let output_file_name = "combined.txt";

    if let Err(e) = append_files(folder_path, output_file_name) {
        eprintln!("Failed to append files: {}", e);
    } else {
        println!("Files successfully appended to '{}'", output_file_name);
    }
}
```

5. We will use a python script to remove data associated with the Part of speech. The script will read the `ngram/combined.txt` file and remove all the data that is associated with a part of speech. The script will then produce a new file called `data.txt` that contains the cleaned data. This assumes that the part of speech is always in the format `word_POS` or `word.n_POS`. To run the script, you can use the following code `python3 wordCompresser4.py` in the terminal.

```python
# Define the function to process the line
def process_line(line):
    # Split the line into words
    words = line.split()
    # Check if there are any words to process
    if not words:
        return None
    # Check if the first word contains '.' or '_'
    if "." not in words[0] and "_" not in words[0]:
        return None  # Skip lines without '.' or '_'
    # Process the first word to remove anything after '.' or '_'
    first_word = words[0].split(".")[0].split("_")[0]
    # Reconstruct the line with the processed first word and the rest of the line
    processed_line = first_word + " " + " ".join(words[1:])
    return processed_line


# Path to the input file
input_file_path = "ngram/combined.txt"
# Path to the output file
output_file_path = "data.txt"

# Open the input file and process it line by line
with open(input_file_path, "r") as input_file, open(
    output_file_path, "w"
) as output_file:
    for line in input_file:
        # Process the current line
        processed_line = process_line(line)
        # Only write the line if it was processed
        if processed_line is not None:
            output_file.write(processed_line + "\n")

print("File has been processed and output saved to:", output_file_path)
```

6. We will use a python script to remove any words that are not in the English language. The script will read the `data.txt` file and remove all the data that is not in the English language. The script will produce a file called `final.txt`. We will use the `nltk` library to check if a word is in the English language. To run the script, you can use the following code `python3 wordCompresser5.py` in the terminal. Before running the script, you need to install the `nltk` library by running `pip install nltk` in the terminal.

```python
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
```

7. We will use a python script to convert the data into a CVS file. The script will read the `final.txt` file and convert it into a CVS file called `data.csv`. The script will produce a CVS file with two columns: `word` and `frequency`. To run the script, you can use the following code `python3 csvConverter.py` in the terminal. The script assumes that the input file is white-space-delimited and contains two columns: `word` and `frequency`. And the output file is a CVS file. The script uses the `csv` module to write the data to the CVS file. The script also assumes that the input file has no header row or comas in the data.

```python
import csv

# Path to the whitespace-delimited input file
input_file_path = "final.txt"
# Path to the output CSV file
output_file_path = "data.csv"

# Open the input and output files
with open(input_file_path, "r") as infile, open(
    output_file_path, "w", newline=""
) as outfile:
    # Create a csv.writer object for writing to the output file
    csv_writer = csv.writer(outfile)

    # Read each line from the input file
    for line in infile:
        # Split the line by whitespace to separate the columns
        columns = line.strip().split()
        # Write the list of columns to the output file as a row in the CSV
        csv_writer.writerow(columns)

print(f"CSV file has been created: {output_file_path}")
```

We will use a python script to aggregate all duplicate words and sum their frequencies and add a header to the CSV file. The script will read the `data.csv` file and aggregate all the duplicate words and sum their frequencies. The script will overwrite the `data.csv` file with the aggregated data and add a header row to the CSV file. To run the script, you can use the following code `python3 aggregate.py` in the terminal.

```python
import csv
from collections import defaultdict

# Path to the input CSV file
input_file_path = "data.csv"
# Path to the output CSV file
output_file_path = "data.csv"

# A dictionary to hold the aggregation of column 2 values for each unique column 1 value
aggregated_data = defaultdict(int)

# Read the CSV file and aggregate the values
with open(input_file_path, mode="r", newline="") as infile:
    csv_reader = csv.reader(infile)
    header = next(csv_reader)  # Skip the header row if your CSV has a header
    for row in csv_reader:
        # Assuming column 1 (index 0) has the key and column 2 (index 1) has the value to be summed
        if row:  # Ensure the row is not empty
            key = row[0]
            value = row[1]
            try:
                # Sum the values for each key
                aggregated_data[key] += int(value)
            except ValueError:
                # Handle the case where the value is not an integer
                print(f"Skipping row with non-integer value: {row}")

# Write the aggregated data to a new CSV file
with open(output_file_path, mode="w", newline="") as outfile:
    csv_writer = csv.writer(outfile)
    csv_writer.writerow(["word", "frequency"])  # Write header to the output file
    for key, sum_value in aggregated_data.items():
        csv_writer.writerow([key, sum_value])

print(f"Aggregated data has been written to {output_file_path}")
```

8. We will use a python script to sort the data in the CSV file by frequency in descending order. The script will read the `data.csv` file and sort the data by frequency in descending order. The script will overwrite the `data.csv` file with the sorted data. To run the script, you can use the following code `python3 sort.py` in the terminal.

```python
import csv
from collections import defaultdict

# Path to the input and output CSV file
file_path = "data.csv"

# A dictionary to hold the aggregation of column 2 values for each unique column 1 value
aggregated_data = defaultdict(int)

# Read the CSV file and aggregate the values
with open(file_path, mode="r", newline="") as infile:
    csv_reader = csv.reader(infile)
    header = next(csv_reader)  # Skip the header row if your CSV has a header
    for row in csv_reader:
        # Assuming column 1 (index 0) has the key and column 2 (index 1) has the value to be summed
        if row:  # Ensure the row is not empty
            key = row[0]
            value = row[1]
            try:
                # Sum the values for each key
                aggregated_data[key] += int(value)
            except ValueError:
                # Handle the case where the value is not an integer
                print(f"Skipping row with non-integer value: {row}")

# Convert the aggregated data into a list of tuples and sort it by the second element (value) in descending order
sorted_data = sorted(aggregated_data.items(), key=lambda item: item[1], reverse=True)

# Write the sorted, aggregated data back to the CSV file
with open(file_path, mode="w", newline="") as outfile:
    csv_writer = csv.writer(outfile)
    csv_writer.writerow(["word", "frequency"])  # Write header to the output file
    for item in sorted_data:
        csv_writer.writerow(item)

print(f"Aggregated and sorted data has been written to {file_path}")
```

9. We now have the final data set in the `data.csv` file. The data set contains two columns: `word` and `frequency`. The data set is now ready for analysis.we can clean the directory by removing the `ngram` directory and the intermediate files. We can also remove the `data.txt` file as it is no longer needed. To clean the directory, you can use the following code `rm data.txt final.txt ngram/* ` in the terminal.

## Summary:

155117 words are in the data set. The data set is now ready for analysis. The data set contains two columns: `word` and `frequency`. The data set is sorted by frequency in descending order. The data set is not comrehensive and may contain errors.
