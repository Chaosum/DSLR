import csv
import os
import sys
import matplotlib.pyplot as plt

def read_csv(filepath):
    data = {}
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # Pour chaque clé, transformer la valeur en float ou None
            for key, value in row.items():
                if key in courses:
                    try:
                        row[key] = float(value) if value != '' else None
                    except ValueError:
                        row[key] = None
                    if key not in data:
                        data[key] = []
                    data[key].append(row[key])
                elif key is "Hogwarts House":
                    if key not in data:
                        data[key] = []
                    data[key].append(row[key])

    return data


def plot_results(data):

    

if (len(sys.argv) > 3):
    print("Wrong arg : expected 'python describe.py filename")
    sys.exit()
if (len(sys.argv) == 1 or os.path.isfile(sys.argv[1]) is False):
    print("using default file ./datasets/dataset_test.csv")
    file = "./datasets/dataset_test.csv"
else :
    file = sys.argv[1]

        courses = [
            "Arithmancy",
            "Astronomy",
            "Herbology",
            "Defense Against the Dark Arts",
            "Divination",
            "Muggle Studies",
            "Ancient Runes",
            "History of Magic",
            "Transfiguration,Potions",
            "Care of Magical Creatures",
            "Charms",
            "Flying"
        ]
        houses = [
           'Grynffindor',
           'Hufflepuff',
           'Ravenclaw',
           'Slytherin'
        ]

data = read_csv(file)
plot_results(data)