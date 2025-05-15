import csv
import os
import sys
from constants import TRAIN_COURSES
import numpy as np


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def read_csv(filepath):
    X = []  # students notes
    students_infos = {"Index": [], "First Name": [], "Last Name": []}
    with open(filepath, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if any(row[course] == "" for course in TRAIN_COURSES):
                continue  # Skip rows with missing values
            try:
                notes = [float(row[course]) for course in TRAIN_COURSES]
            except:
                continue  # Skip rows with wrong float values
            students_infos["Index"].append(row["Index"])
            students_infos["First Name"].append(row["First Name"])
            students_infos["Last Name"].append(row["Last Name"])
            X.append(notes)

    return np.array(X), students_infos


def read_train_result(filepath):
    with open("weights.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        # Lire les thetas
        thetas = []
        houses = []
        for row in reader:
            if row[0] == "Mean":
                mean = np.array([float(x) for x in row[1:]])
            elif row[0] == "Std":
                std = np.array([float(x) for x in row[1:]])
            else:
                houses.append(row[0])
                thetas.append([float(x) for x in row[1:]])
        thetas = np.array(thetas)
    return thetas, houses, mean, std


def normalize(X, mean, std):
    return (X - mean) / std


if __name__ == "__main__":
    if (
        len(sys.argv) == 3
        and os.path.isfile(sys.argv[1]) is True
        and os.path.isfile(sys.argv[2]) is True
    ):
        data_file = sys.argv[1]
        thetas_files = sys.argv[2]
    else:
        print("Wrong arg : expected 'python logreg_predict.py dataFile weightsFile")
        sys.exit()
    X_raw, students_infos = read_csv(data_file)

    thetas, houses, mean, std = read_train_result(thetas_files)

    X = normalize(X_raw, mean, std)

    X = np.c_[np.ones((X.shape[0], 1)), X]
    results = []
    i = 0
    for x in X:
        z = np.dot(thetas, x)
        prediction = sigmoid(z)
        idx = np.argmax(prediction)
        predicted_house = houses[idx]
        results.append(predicted_house)
    with open("houses.csv", mode="w", newline="") as resultFile:
        writer = csv.writer(resultFile)
        for i, house in enumerate(results):
            writer.writerow([students_infos["Index"][i], house])
