import csv
from global_variable import houses, courses, housesColor

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

def histogram(data, course, ax):
    for house in houses:
        notes = [x for x in data[house][course] if x is not None]
        if notes:
            ax.hist(notes, bins=10, alpha=0.5,
                    edgecolor=housesColor["edge" + house],
                    color=housesColor[house],
                    label=house)
    return

def scatter_plot(data, feature1, feature2, ax):
    for house in houses:
        valid_data = [
            (x, y) for x, y in zip(data[house][feature1], data[house][feature2])
            if x is not None and y is not None
        ]
        if valid_data:
            notes1, notes2 = zip(*valid_data)
            ax.scatter(notes1, notes2, alpha=0.3, label=house,
                       edgecolors=housesColor["edge" + house],
                       color=housesColor[house], s=10)
    return
