import pandas as pd

# Open the processed_combined.txt file for reading
with open("processed_combined.txt", "r") as txt_file:
    # Read the contents of the file
    txt_content = txt_file.read()

# Replace spaces with commas
csv_content = txt_content.replace(" ", ",")

# Write the modified content to a CSV file
with open("data.csv", "w") as csv_file:
    csv_file.write(csv_content)

print("Conversion completed. The result is saved in data.csv.")

# Read the CSV file into a pandas DataFrame
df = pd.read_csv("data.csv", header=None)

# Get the shape of the DataFrame
csv_shape = df.shape

print("Shape of the CSV file:", csv_shape)
