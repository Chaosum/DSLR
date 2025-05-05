import csv
from global_variable import houses, courses

def read_csv_split_houses(filepath):
    data = {}
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for house in houses:
            data[house] = {}
        for row in reader:
            # Pour chaque clé, transformer la valeur en float ou None
            for key, value in row.items():
                if key in courses:
                    try:
                        row[key] = float(value) if value != '' else None
                    except ValueError:
                        row[key] = None
                if key not in data[row["Hogwarts House"]]:
                    data[row["Hogwarts House"]][key] = []
                data[row["Hogwarts House"]][key].append(row[key])
    return data