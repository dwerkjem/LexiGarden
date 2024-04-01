import pandas as pd

# Define the input and output CSV file names
input_csv_file = "ngram/final.csv"
output_csv_file = "sorted.csv"

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(input_csv_file)

# Sort the DataFrame by the second column (Note: columns are zero-indexed in pandas)
# Replace 'Column2Name' with the actual name of the second column if it has a header,
# or use df.columns[1] if you're unsure of the name or it doesn't have one
df_sorted = df.sort_values(by=df.columns[1])

# Write the sorted DataFrame back to a new CSV file
df_sorted.to_csv(output_csv_file, index=False)

print(f"Data sorted by the second column and saved to {output_csv_file}.")
