import csv
import sys
import os
import math

def is_float(value):
    try:
        float(value)
        return True
    except:
        return False

def read_csv(filepath):
    data = {}
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            # Pour chaque clé, transformer la valeur en float ou None
            for key, value in row.items():
                try:
                    row[key] = float(value) if value != '' else None
                except ValueError:
                    pass
                
                if key not in data:
                    data[key] = []
                data[key].append(row[key])

    return data

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


def getStd(data):
    size = len(data)
    mean = sum(data) / size
    std = math.sqrt((sum(x * x for x in data) / size) - (mean ** 2))
    return std

def getPercentile(percent, data):
    data = sorted(data)
    n = len(data)
    i = (percent/100) * (n - 1)
    #interpolation
    lower = math.floor(i)
    upper = math.ceil(i)
    percentile = data[lower] * (upper - i) + data[upper] * (i - lower) 
    return percentile

def getMin(data):
    min_value = data[0]
    for element in data[1:]:
        if element < min_value:
            min_value = element
    return min_value

def getMax(data):
    max_value = data[0]
    for element in data[1:]:
        if element > max_value:
            max_value = element
    return max_value


def describe(data, numeric_col):
    results = {}
    results["Count"]  = {}
    results["Mean"] = {}
    results["Std"] = {}
    results["Min"] = {}
    results["25%"] = {}
    results["50%"] = {}
    results["75%"] = {}
    results["Max"] = {}
    for col in numeric_col:
        filtered_data = [value for value in data[col] if value is not None]
        if not data:
            continue
        results["Count"][col] = len(filtered_data)
        results["Mean"][col] = sum(filtered_data) / results["Count"][col]
        results["Std"][col] = getStd(filtered_data)
        results["Min"][col] = getMin(filtered_data)
        results["25%"][col] = getPercentile(25, filtered_data)
        results["50%"][col] = getPercentile(50, filtered_data)
        results["75%"][col] = getPercentile(75, filtered_data)
        results["Max"][col] = getMax(filtered_data)
    print_stats(results, numeric_col)

def print_stats(describe_result, numeric_col):
    # angle haut gauche
    print(f"{'':<{getMax([len(key) for key in describe_result.keys()])}}", end='')
    # Cols
    for stat in numeric_col:
        print(f"{stat:>{len(stat) if len(stat) >= 15 else 15}}", end='\t')
    print()  # Saut de ligne après le header

    # Print les résultats pour chaque feature
    for feature, stats in describe_result.items():
        print(f"{feature:<{getMax([len(key) for key in describe_result.keys()])}}", end='')

        # Affichage des résultats pour chaque statistique avec 6 décimales
        for stat in stats:
            print(f"{stats[stat]:>{len(stat) if len(stat) >= 15 else 15}.6f}", end='\t')  # Formatage à 6 décimales
        print()

if (len(sys.argv) > 3):
    print("Wrong arg : expected 'python describe.py filename")
    sys.exit()
if (os.path.isfile(sys.argv[1]) is False):
    print("file {sys.argv[1]} not found defaulting to ./datasets/dataset_test.csv")
    file = "./datasets/dataset_test.csv"
else :
    file = sys.argv[1]

data = read_csv(file)
numeric_cols = detect_numeric_columns(data)
describe(data, numeric_cols)