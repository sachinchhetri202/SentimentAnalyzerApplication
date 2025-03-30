# review_fetcher.py
#
# This file contains a simple function to load reviews from a CSV file.
# It uses the pandas library to read the CSV file, automatically parsing the "date" column.
# The CSV is expected to have columns such as "date", "rating", and "review".
# If the file is loaded successfully, the function returns a pandas DataFrame.
# Otherwise, it prints an error message and returns None.
#
# You can run this file directly to see a preview (first few rows) of the loaded reviews.

import pandas as pd

def fetch_reviews(file_path="Reviews.csv"):
    """
    Fetch reviews from a CSV file.

    Parameters:
        file_path (str): The path to the CSV file containing reviews.
                         Defaults to "Reviews.csv".

    Returns:
        pd.DataFrame: A DataFrame containing the reviews data, with the "date" column
                      parsed as datetime objects. Expected columns include "date", "rating",
                      and "review".
        If there is an error reading the file, prints the error and returns None.
    """
    try:
        # Attempt to read the CSV file while parsing the "date" column as datetime objects.
        df = pd.read_csv(file_path, parse_dates=["date"])
        return df
    except Exception as e:
        # If any error occurs (file not found, parsing error, etc.), print the error message.
        print("Error reading the file:", e)
        return None

# When this file is run as a standalone program, print the first few rows of the DataFrame.
if __name__ == "__main__":
    df = fetch_reviews()
    if df is not None:
        # Display the top 5 rows to quickly verify that the data loaded correctly.
        print(df.head())
    else:
        print("No data to display.")
