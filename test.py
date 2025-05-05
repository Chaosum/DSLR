import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

# Exemple de données : notes pour différentes matières
data = {
    'Arithmancy': np.random.uniform(0, 100, 50),
    'Astronomy': np.random.uniform(0, 100, 50),
    'Herbology': np.random.uniform(0, 100, 50),
    'Defense Against the Dark Arts': np.random.uniform(0, 100, 50),
}

# Liste des matières disponibles pour le menu déroulant
courses = list(data.keys())

# Créer la figure et l'axe
fig, ax = plt.subplots(figsize=(8, 6))
plt.subplots_adjust(bottom=0.25)

# Initialiser l'histogramme avec la première matière
course = courses[0]
hist_data = data[course]
n, bins, patches = ax.hist(hist_data, bins=10, edgecolor='black')

# Ajouter des labels et un titre
ax.set_title(f"Distribution des notes pour {course}")
ax.set_xlabel('Notes')
ax.set_ylabel("Nombre d'élèves")

# Créer une fonction pour mettre à jour l'histogramme
def update(val):
    course = course_selector.val
    ax.clear()  # Effacer l'ancienne figure
    hist_data = data[course]
    ax.hist(hist_data, bins=10, edgecolor='black')
    ax.set_title(f"Distribution des notes pour {course}")
    ax.set_xlabel('Notes')
    ax.set_ylabel("Nombre d'élèves")
    fig.canvas.draw_idle()

# Créer un slider pour sélectionner la matière (menu déroulant)
course_selector = Slider(ax=fig.add_axes([0.2, 0.01, 0.65, 0.03]),  # Position du slider
                         label="Matière", 
                         valmin=0, 
                         valmax=len(courses)-1, 
                         valinit=0,
                         valstep=1)

# Ajouter une fonction de mise à jour au slider
course_selector.on_changed(update)

# Afficher le graphique
plt.show()
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Exemple de données : notes pour différentes matières
data = {
    'Arithmancy': np.random.uniform(0, 100, 50),
    'Astronomy': np.random.uniform(0, 100, 50),
    'Herbology': np.random.uniform(0, 100, 50),
    'Defense Against the Dark Arts': np.random.uniform(0, 100, 50),
}

# Fonction pour mettre à jour l'histogramme
def update_plot(event):
    course = course_combobox.get()  # Récupère la matière sélectionnée
    hist_data = data[course]
    
    # Efface le graphique précédent
    ax.clear()
    ax.hist(hist_data, bins=10, edgecolor='black')
    ax.set_title(f"Distribution des notes pour {course}")
    ax.set_xlabel('Notes')
    ax.set_ylabel("Nombre d'élèves")
    
    # Redessine le graphique dans la fenêtre Tkinter
    canvas.draw()

# Créer la fenêtre Tkinter
root = tk.Tk()
root.title("Histogramme des notes des matières")

# Création du combobox (menu déroulant) pour sélectionner la matière
course_combobox = ttk.Combobox(root, values=list(data.keys()))
course_combobox.set(list(data.keys())[0])  # Matière par défaut
course_combobox.pack(pady=10)

# Bouton pour mettre à jour le graphique
update_button = tk.Button(root, text="Mettre à jour", command=update_plot)
update_button.pack(pady=5)

# Créer la figure et l'axe
fig, ax = plt.subplots(figsize=(8, 6))

# Afficher l'histogramme de la première matière
initial_course = list(data.keys())[0]
initial_data = data[initial_course]
ax.hist(initial_data, bins=10, edgecolor='black')
ax.set_title(f"Distribution des notes pour {initial_course}")
ax.set_xlabel('Notes')
ax.set_ylabel("Nombre d'élèves")

# Ajouter le graphique Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Lier la mise à jour du graphique au changement de matière
course_combobox.bind("<<ComboboxSelected>>", update_plot)

# Lancer l'interface Tkinter
root.mainloop()
