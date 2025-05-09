import csv
import sys
from global_variable import train_courses as courses, houses
import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

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

file = "./datasets/dataset_train.csv"
X_raw, y = read_csv(file)


#on recupere les notes non normalisé et la maison dans lequel le student est présent sour la forme [1 0 0 0]
X, mean, std = normalize(X_raw)
#ajoute une matrice remplis de 1 et de taille (X.shape[0] 1) avant la matrice X
X = np.c_[np.ones((X.shape[0], 1)), X]
# setup grand θ
thetas = np.zeros((len(houses), X.shape[1]))

increment = 0.1

print("Training in progress ...")
try :
    sufficient_accuracy = False
    iteration = 1
    while not sufficient_accuracy and iteration < 100:
        print(f"\rTraining in progress ... epoch {iteration}")
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
            #on modifie les thetas en fonction du gradient trouvé
            thetas -= increment * gradient
            if np.isnan(thetas).any():
                raise ValueError("Erreur : NaN in thetas !")
        predictions = sigmoid(np.dot(X, thetas.T))
        #la position entre 0 et 3 de la plus grande prediction qu'on a faite
        predicted_labels = np.argmax(predictions, axis=1)
        #la position entre 0 et 3 de la maison réel
        true_labels = np.argmax(y, axis=1)

        predictions = sigmoid(np.dot(X, thetas.T))
        predicted_labels = np.argmax(predictions, axis=1)
        true_labels = np.argmax(y, axis=1)

        # Accuracy globale
        accuracy = np.mean(predicted_labels == true_labels)
        print(f"Global accuracy: {accuracy:.2%}")
        sufficient_accuracy = accuracy >= 0.98
            
    with open("weights.csv", mode="w", newline='') as resultFile:
        writer = csv.writer(resultFile)

        # En-têtes
        writer.writerow(["House"] + [f"Theta{i}" for i in range(thetas.shape[1])])

        # Poids pour chaque maison
        for i, house in enumerate(houses):
            writer.writerow([house] + list(thetas[i]))

        # Ajoute les vecteurs de normalisation
        writer.writerow(["Mean"] + list(mean))
        writer.writerow(["Std"] + list(std))
        print("\nTraining done ✅")

except Exception as e:
    print(f"\rTraining failed ❌: {e}")

