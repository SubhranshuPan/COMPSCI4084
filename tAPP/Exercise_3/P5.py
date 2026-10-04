while True:
    filename = input("Enter filename: ")

    try:
        file = open(filename, "r")
        contents = file.read()
        print(contents)
        file.close()
        break

    except FileNotFoundError:
        print("File not found, try again")

# import pandas as pd

# df = pd.read_csv("Data.csv", parse_dates=['Date'])

# most_recent_years = df['Date'].dt.year.max()
# df_recent = df[df['Date'].dt.year == most_recent_years]

# print(df_recent.head())
