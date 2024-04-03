import pandas as pd

# Read the CSV file into a pandas DataFrame
df = pd.read_csv("cleaned_data.csv")

# Get the shape of the DataFrame
csv_shape = df.shape

print("Shape of the CSV file:", csv_shape)
