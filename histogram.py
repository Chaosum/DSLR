import csv, os, sys
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from global_variable import houses, housesColor, courses
from plot_utils import read_csv_split_houses

if (len(sys.argv) > 3):
    print("Wrong arg : expected 'python describe.py filename")
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
root.title("Score distribution between houses")

course_combobox = ttk.Combobox(root, values=list(courses))
course_combobox.set(list(courses)[10])  # Matière par défaut creature magique => la plus homogene
course_combobox.pack(pady=10)

def histogram(data, course, houses, housesColor):
    ax.clear()
    for house in houses:
        notes = [x for x in data[house][course] if x is not None]
        if notes:  # évite de tracer un hist vide
            ax.hist(notes, bins=10, alpha=0.5, edgecolor=housesColor["edge" + house], color=housesColor[house], label=house)
    ax.set_title(f"Distribution des notes pour {course}")
    ax.set_xlabel("Notes")
    ax.set_ylabel("Nombre d'élèves")
    ax.legend()

fig, ax = plt.subplots(figsize=(8, 6))
initial_course = list(courses)[10]
histogram(data, initial_course, houses, housesColor)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

def update_plot(event=None):
    course = course_combobox.get()
    histogram(data, course, houses, housesColor)
    canvas.draw()

course_combobox.bind("<<ComboboxSelected>>", update_plot)

root.mainloop()
