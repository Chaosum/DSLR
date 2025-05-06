import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def compute_cost(X, y, theta):
    m = len(y)
    h = sigmoid(X.dot(theta))  # Prédiction avec sigmoïde
    cost = (-y.T.dot(np.log(h)) - (1 - y).T.dot(np.log(1 - h))) / m
    return cost

def gradient_descent(X, y, theta, alpha, iterations):
    m = len(y)
    cost_history = []

    for i in range(iterations):
        h = sigmoid(X.dot(theta))  # Prédiction
        gradients = X.T.dot(h - y) / m  # Calcul du gradient
        theta -= alpha * gradients  # Mise à jour des theta
        cost_history.append(compute_cost(X, y, theta))  # Historique du coût

    return theta, cost_history

# Exemple d'utilisation avec des données d'entraînement (X, y)
# X = matrice des caractéristiques, y = vecteur des étiquettes
X = np.array([[1, 50, 60], [1, 60, 70], [1, 70, 80]])  # Exemple avec 3 élèves et 2 caractéristiques
y = np.array([1, 0, 1])  # Gryffindor, Non Gryffindor, Gryffindor (0 ou 1)
theta = np.zeros(X.shape[1])  # Initialisation des theta
alpha = 0.01  # Taux d'apprentissage
iterations = 1000  # Nombre d'itérations

# Apprentissage
theta, cost_history = gradient_descent(X, y, theta, alpha, iterations)

# Affichage du coût pour chaque itération
print("Final theta:", theta)
print("Coût final:", cost_history[-1])
