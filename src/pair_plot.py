import os
import sys
import matplotlib.pyplot as plt
from global_variable import houses, housesColor, courses
from plot_utils import read_csv_split_houses, histogram, scatter_plot

if (len(sys.argv) > 2):
    print("Wrong arg : expected 'python describe.py [filename]")
    sys.exit()
if (len(sys.argv) == 2 and os.path.isfile(sys.argv[1]) is True):
    file = sys.argv[1]
else :
    print("using default file ./src/datasets/dataset_train.csv")
    file = "./src/datasets/dataset_train.csv"

file = "./src/datasets/dataset_train.csv"
data = read_csv_split_houses(file)

n = len(courses)

fig, axes = plt.subplots(n, n, figsize=(n*1.6, n*1.6))

handles = []  # Liste pour stocker les objets graphiques de la légende
labels = []   # Liste pour les labels uniques

for i in range(n):
    for j in range(n):
        ax = axes[i, j]
        if i == j:
            histogram(data, courses[i], ax)
        else:
            scatter_plot(data, courses[i], courses[j], ax)
        if i == n - 1:  # Pour les titres des axes horizontaux
            ax.set_xlabel(courses[j], rotation=45, ha='right', fontsize=10)
        if j == 0:  # Pour les titres des axes verticaux
            ax.set_ylabel(courses[i], rotation=0, ha='right', fontsize=10)
        if i < n - 1:
            ax.set_xticks([])
        if j > 0:
            ax.set_yticks([])
        ax.tick_params(axis='both', which='major', labelsize=8)

legend_handles = []
for house in houses:
    if house not in [handle.get_label() for handle in legend_handles]:
        # Crée un scatter avec un label unique
        handle = ax.scatter([], [], color=housesColor[house], label=house, alpha=0.5)
        legend_handles.append(handle)
# Affichage de la légende unique (en dehors du graphique)
fig.legend(handles=legend_handles, loc='center right', bbox_to_anchor=(1, 0.5))

fig.suptitle('Pair Plot des Matières', fontsize=16)
plt.subplots_adjust(hspace=0.2, wspace=0.2, top=0.95 ,bottom=0.21, left=0.15)
plt.show()
