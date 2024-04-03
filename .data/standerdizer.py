def standardize_data(data):
    # remove any leading or trailing white spaces and quotes
    data = data.strip()
    data = data.replace('"', "")
    return data


def standardize_file(file_path):
    # read
    with open(file_path, "r") as file:
        data = file.read()
        # standardize
        data = standardize_data(data)
    # write
    with open(file_path, "w") as file:
        file.write(data)


if __name__ == "__main__":
    standardize_file("data.csv")
