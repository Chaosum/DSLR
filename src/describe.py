import csv
import sys
import os
import pandas as pd

from utils import get_std, get_min, get_percentile, get_max, read_csv


def is_float(value):
    try:
        float(value)
        return True
    except:
        return False


def detect_numeric_columns(data_by_column):
    numeric_columns = []
    for col, values in data_by_column.items():
        numeric_count = 0
        total_count = 0
        for v in values:
            if v != "":
                total_count += 1
                if is_float(v):
                    numeric_count += 1
        if total_count > 0 and numeric_count / total_count > 0.95:
            numeric_columns.append(col)

    return numeric_columns


def describe(data, numeric_col):
    results = {
        "Count": {},
        "Mean": {},
        "Std": {},
        "Min": {},
        "25%": {},
        "50%": {},
        "75%": {},
        "Max": {},
        "Missing": {},
        "Range": {},
    }
    for col in numeric_col:
        filtered_data = [value for value in data[col] if value is not None]
        missing_number = len(data[col]) - len(filtered_data)
        if not data:
            continue
        results["Count"][col] = len(filtered_data)
        results["Mean"][col] = sum(filtered_data) / results["Count"][col]
        results["Std"][col] = get_std(filtered_data)
        results["Min"][col] = get_min(filtered_data)
        results["25%"][col] = get_percentile(25, filtered_data)
        results["50%"][col] = get_percentile(50, filtered_data)
        results["75%"][col] = get_percentile(75, filtered_data)
        results["Max"][col] = get_max(filtered_data)
        results['Missing'][col] = missing_number
        results['Range'][col] = results['Max'][col] - results['Min'][col]
    print_stats(results, numeric_col)


def print_stats(describe_result, numeric_col):
    with open("describe.csv", mode="w", newline="") as f:
        for stat in numeric_col:
            f.write(f"{stat},")
        f.write('\n')

        for feature, stats in describe_result.items():
            f.write(f"{feature},")

            for stat in stats:
                f.write(f"{stats[stat]},")
            f.write('\n')


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Wrong arg : expected 'python describe.py [filename]")
        sys.exit()
    if len(sys.argv) == 2 and os.path.isfile(sys.argv[1]) is True:
        file = sys.argv[1]
    else:
        print("using default file ./src/datasets/dataset_train.csv")
        file = "./src/datasets/dataset_train.csv"
    data = read_csv(file)
    if data is None:
        print("No data found")
        sys.exit(1)
    numeric_cols = detect_numeric_columns(data)

    describe(data, numeric_cols)