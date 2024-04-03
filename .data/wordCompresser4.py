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
