import os
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from global_variable import houses, housesColor, courses
from plot_utils import read_csv_split_houses, scatter_plot
import tkinter as tk
from tkinter import ttk

if (len(sys.argv) > 2):
    print("Wrong arg : expected 'python describe.py [filename]")
    sys.exit()
if (len(sys.argv) == 2 and os.path.isfile(sys.argv[1]) is True):
    file = sys.argv[1]
else :
    print("using default file ./src/datasets/dataset_train.csv")
    file = "./src/datasets/dataset_train.csv"

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



fig, ax = plt.subplots(figsize=(8, 6))

initialFeature1 = course_combobox1.get()
initialFeature2 = course_combobox2.get()
ax.clear()
scatter_plot(data, initialFeature1, initialFeature2, ax)
ax.set_title(f"{initialFeature1} vs {initialFeature2}")
ax.set_xlabel(initialFeature1)
ax.set_ylabel(initialFeature2)
ax.legend()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

def update_plot(event=None):
    feature1 = course_combobox1.get()
    feature2 = course_combobox2.get()
    ax.clear()
    scatter_plot(data, feature1, feature2, ax)
    ax.set_title(f"{feature1} vs {feature2}")
    ax.set_xlabel(feature1)
    ax.set_ylabel(feature2)
    ax.legend()
    canvas.draw()


root.mainloop()
