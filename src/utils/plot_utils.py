import csv
import os

from constants import HOUSES, HOUSES_COLOR, COURSES


def read_csv_split_houses(filepath):
    if not os.path.isfile(filepath):
        return None
    data = {}
    with open(filepath, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for house in HOUSES:
            data[house] = {}
        for row in reader:
            # Pour chaque clé, transformer la valeur en float ou None
            for key, value in row.items():
                if key in COURSES:
                    try:
                        row[key] = float(value) if value != "" else None
                    except ValueError:
                        row[key] = None
                if key not in data[row["Hogwarts House"]]:
                    data[row["Hogwarts House"]][key] = []
                data[row["Hogwarts House"]][key].append(row[key])
    return data


def histogram(data, course, ax):
    for house in HOUSES:
        notes = [x for x in data[house][course] if x is not None]
        if notes:
            ax.hist(
                notes,
                bins=10,
                alpha=0.5,
                edgecolor=HOUSES_COLOR["edge" + house],
                color=HOUSES_COLOR[house],
                label=house,
            )
    return


def scatter_plot(data, feature1, feature2, ax):
    for house in HOUSES:
        valid_data = [
            (x, y)
            for x, y in zip(data[house][feature1], data[house][feature2])
            if x is not None and y is not None
        ]
        if valid_data:
            notes1, notes2 = zip(*valid_data)
            ax.scatter(
                notes1,
                notes2,
                alpha=0.3,
                label=house,
                edgecolors=HOUSES_COLOR["edge" + house],
                color=HOUSES_COLOR[house],
                s=10,
            )
    return
