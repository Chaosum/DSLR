import csv
import os
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from global_variable import houses, housesColor, courses
from plot_utils import read_csv_split_houses
import tkinter as tk
from tkinter import Canvas, ttk

if (len(sys.argv) > 3):
    print("Wrong arg : expected 'python describe.py [filename]")
    sys.exit()
if (len(sys.argv) == 1 or os.path.isfile(sys.argv[1]) is False):
    print("using default file ./datasets/dataset_train.csv")
    file = "./datasets/dataset_train.csv"
else :
    file = sys.argv[1]

data = read_csv_split_houses(file)

def on_closing():
    root.destroy()
    sys.exit(0)

root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.title("Features similarity")

error_label = tk.Label(root, text="", fg="red")
error_label.pack()

def on_first_select(event):
    # Empêcher la sélection de la même matière dans le second Combobox
    selected_course = course_combobox1.get()
    # Si la sélection actuelle dans le second Combobox est invalide, le réinitialiser
    if course_combobox2.get() == selected_course  or course_combobox2.get() == '':
        course_combobox2.set('')  # ou tu peux remettre une valeur par défaut
        error_label.config(text="Vous ne pouvez pas sélectionner la même matière dans les deux champs.")
    else:
        error_label.config(text="")
        update_plot()

def on_second_select(event):
    # Empêcher la sélection de la même matière dans le premier Combobox
    selected_course = course_combobox2.get()
    # Si la sélection actuelle dans le premier Combobox est invalide, le réinitialiser
    if course_combobox1.get() == selected_course or course_combobox1.get() == '':
        course_combobox1.set('')  # ou tu peux remettre une valeur par défaut
        error_label.config(text="Vous ne pouvez pas sélectionner la même matière dans les deux champs.")
    else:
        error_label.config(text="")
        update_plot()
        

# Création du premier Combobox
course_combobox1 = ttk.Combobox(root, values=courses)
course_combobox1.set(courses[0])  # Matière par défaut
course_combobox1.pack(pady=10)
course_combobox1.bind("<<ComboboxSelected>>", on_first_select)

# Création du deuxième Combobox
course_combobox2 = ttk.Combobox(root, values=courses)
course_combobox2.set(courses[1])  # Matière par défaut
course_combobox2.pack(pady=10)
course_combobox2.bind("<<ComboboxSelected>>", on_second_select)

def scatter_plot(feature1, feature2):
    ax.clear()
    for house in houses:
        # Créer une liste de paires de (feature1, feature2) pour chaque étudiant dans cette maison
        valid_data = [(x, y) for idx, (x, y) in enumerate(zip(data[house][feature1], data[house][feature2])) if x is not None and y is not None]
        
        # Si valid_data n'est pas vide, extraire les notes correspondantes
        if valid_data:
            notes1, notes2 = zip(*valid_data)  # Dézipper en deux listes : notes1 et notes2
            plt.scatter(notes1, notes2, alpha=0.3, label=house, edgecolors=housesColor["edge" + house], color=housesColor[house])
        else:
            print(f"Warning: No valid data for {house}, skipping this house.")

    ax.set_title(f"{feature1} vs {feature2}")
    ax.set_xlabel(feature1)
    ax.set_ylabel(feature2)
    ax.legend()

fig, ax = plt.subplots(figsize=(8, 6))

initialFeature1 = course_combobox1.get()
initialFeature2 = course_combobox2.get()

scatter_plot(initialFeature1, initialFeature2)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

def update_plot(event=None):
    feature1 = course_combobox1.get()
    feature2 = course_combobox2.get()
    scatter_plot(feature1, feature2)
    canvas.draw()


root.mainloop()
