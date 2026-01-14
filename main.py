
import csv
import pandas as pd
from pathlib import Path

data_dir = Path("./data/chegadas_2024.csv")

#Reads the csv file with encoding iso-8859-1 as a pandas dataframe and prints the first 5 rows
def view_csv(file_path: Path):

    df = pd.read_csv(file_path, encoding="iso-8859-1", sep=";")
    print(df.tail())

def main():
    view_csv(data_dir)


if __name__ == "__main__":
    main()
