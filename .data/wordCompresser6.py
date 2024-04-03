import csv


def verify_csv(input_file, output_file):
    with open(input_file, "r") as csvfile:
        reader = csv.reader(csvfile)
        rows = []
        for row in reader:
            # Remove extra commas and join the cells with a single comma
            cleaned_row = ",".join(cell.strip() for cell in row if cell.strip())
            rows.append(cleaned_row)

    # Write the cleaned data to a new CSV file
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for row in rows:
            writer.writerow([row])  # Writing each row as a list to maintain CSV format


if __name__ == "__main__":
    input_file = "data.csv"  # Change this to your CSV file
    output_file = "cleaned_data.csv"  # Output file name

    verify_csv(input_file, output_file)
    print("CSV verification completed. The cleaned data is saved in", output_file)
