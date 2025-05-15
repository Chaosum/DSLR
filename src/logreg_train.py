import csv
import os
import sys
from constants import COURSES, HOUSES
import numpy as np

from utils import get_mean, get_std


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def read_csv(filepath):
    X = []  # students notes
    y = []
    with open(filepath, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if any(row[course] == "" for course in COURSES):
                continue  # Skip rows with missing values
            try:
                notes = [float(row[course]) for course in COURSES]
            except:
                continue  # Skip rows with wrong float values
            X.append(notes)

            # Créer le label one-hot
            student_house = [
                1 if row["Hogwarts House"] == house else 0 for house in HOUSES
            ]
            y.append(student_house)
    return np.array(X), np.array(y)


def normalize(X):
    X = np.array(X, dtype=float)
    n_samples, n_features = X.shape
    mean = []
    std = []

    for i in range(n_features):
        col = X[:, i].tolist()  # Convertit la colonne en liste Python
        col_mean = get_mean(col)
        col_std = get_std(col)
        mean.append(col_mean)
        std.append(col_std)

    mean = np.array(mean)
    std = np.array(std)
    return (X - mean) / std, mean, std


if __name__ == "__main__":
    if ( 
        len(sys.argv) == 2
        and os.path.isfile(sys.argv[1]) is True
    ):
        file = sys.argv[1]
    else:
        print("Wrong arg : expected 'python logregtrain.py datasetpath.csv")
        sys.exit()
    try :
        X_raw, y = read_csv(file)
    except Exception as e:
        print(f"Erreur while parsing the file {file}")
        sys.exit()
    X, mean, std = normalize(X_raw)
    X = np.c_[np.ones((X.shape[0], 1)), X]
    thetas = np.zeros((len(HOUSES), X.shape[1]))

    increment = 0.1

    print("Training in progress ...",end='')
    try:
        sufficient_accuracy = False
        iteration = 1
        while not sufficient_accuracy and iteration < 100:
            print(f"\rTraining in progress ... epoch {iteration}", end='')
            iteration = iteration + 1
            old_thetas = thetas.copy()
            for i in np.random.permutation(len(X)):
                x = X[i]
                # z = θ * xi = θi0 * 1 + θi1 * xi1 + θi2 * xi2 ... θin * xin
                # sachant que thetas est de taille 4 car 4 houses on gagne du temps en faisant le dot product thetas . x
                z = np.dot(thetas, x)
                # la prediction ŷ = σ(z) = σ(θ * xi)
                prediction = sigmoid(z)
                error = prediction - y[i]
                # produit exterieur l'erreur (yi - ŷi) * xij avec xij = la note dans une matiere
                gradient = np.outer(error, x)
                # on modifie les thetas en fonction du gradient trouvé
                thetas -= increment * gradient
                if np.isnan(thetas).any():
                    raise ValueError("Erreur : NaN in thetas !")
            predictions = sigmoid(np.dot(X, thetas.T))
            # la position entre 0 et 3 de la plus grande prediction qu'on a faite
            predicted_labels = np.argmax(predictions, axis=1)
            # la position entre 0 et 3 de la maison réel
            true_labels = np.argmax(y, axis=1)

            # Accuracy globale
            accuracy = np.mean(predicted_labels == true_labels)
            print(f"\nGlobal accuracy: {accuracy:.2%}")
            sufficient_accuracy = accuracy >= 0.98

        with open("weights.csv", mode="w", newline="") as resultFile:
            writer = csv.writer(resultFile)

            # En-têtes
            writer.writerow(["House"] + [f"Theta{i}" for i in range(thetas.shape[1])])

            # Poids pour chaque maison
            for i, house in enumerate(HOUSES):
                writer.writerow([house] + list(thetas[i]))

            # Ajoute les vecteurs de normalisation
            writer.writerow(["Mean"] + list(mean))
            writer.writerow(["Std"] + list(std))
            print("\nTraining done ✅")

    except Exception as e:
        print(f"\rTraining failed ❌: {e}")
