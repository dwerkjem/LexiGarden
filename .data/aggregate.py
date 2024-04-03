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
