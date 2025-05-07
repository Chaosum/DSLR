import csv
import sys
from global_variable import courses, houses
import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

"""
students_notes: X
"""
def read_csv(filepath):
    X = [] # students notes
    y = []
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if any(row[course] == '' for course in courses):
                continue  # Skip rows with missing values
            try:
                notes = [float(row[course]) for course in courses] 
            except:
                continue # Skip rows with wrong float values
            X.append(notes)

            # Créer le label one-hot
            student_house = [1 if row["Hogwarts House"] == house else 0 for house in houses]
            y.append(student_house)
    return np.array(X), np.array(y)

def normalize(X):
    mean = np.mean(X, axis=0) #TODOO a voir avec le sujet si faut pas recoder ca
    std = np.std(X, axis=0) #TODOO a voir avec le sujet si faut pas recoder ca
    return (X - mean) / std, mean, std

file = "./src/datasets/dataset_train.csv"
X_raw, y = read_csv(file)


#on recupere les notes non normalisé et la maison dans lequel le student est présent sour la forme [1 0 0 0]
X, mean, std = normalize(X_raw)
#ajoute une matrice remplis de 1 et de taille (X.shape[0] 1) avant la matrice X
X = np.c_[np.ones((X.shape[0], 1)), X]
# setup grand θ
thetas = np.zeros((len(houses), X.shape[1]))

increment = 0.1
iteration = 1000

print("Training in progress ...")
try :
    for _ in range(iteration):
        for i in range(len(X)):
            x = X[i]
            # z = θ * xi = θi0 * 1 + θi1 * xi1 + θi2 * xi2 ... θin * xin 
            # sachant que thetas est de taille 4 car 4 houses
            z = np.dot(thetas, x)
            # ŷ = σ(θ * xi) = σ(z)
            prediction = sigmoid(z)
            error = prediction - y[i]
            gradient = np.outer(error, x)  # produit exterieur ()
            thetas -= increment * gradient
            if np.isnan(thetas).any():
                raise ValueError("Erreur : NaN in thetas !")
    with open("weights.csv", mode="w", newline='') as resultFile:
        writer = csv.writer(resultFile)
        writer.writerow(["House"] + [f"Theta{i}" for i in range(thetas.shape[1])])
        for i, house in enumerate(houses):
            writer.writerow([house] + list(thetas[i]))
    print("Training done ✅")

except Exception as e:
    print("\rTraining failed ❌: {e.message}")

