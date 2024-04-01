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
done

echo "All downloads completed."

