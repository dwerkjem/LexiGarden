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
