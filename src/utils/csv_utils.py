import csv
import os


def read_csv(filepath):
    data = {}
    if not os.path.isfile(filepath):
        return None
    with open(filepath, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for key, value in row.items():
                try:
                    row[key] = float(value) if value != "" else None
                except ValueError:
                    pass

                if key not in data:
                    data[key] = []
                data[key].append(row[key])

    return data
