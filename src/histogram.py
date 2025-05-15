import os
import sys
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from constants.global_variable import COURSES
from utils import read_csv_split_houses, histogram


def on_closing():
    root.destroy()
    sys.exit(0)


def update_plot(event=None):
    course = course_combobox.get()
    ax.clear()
    histogram(data, course, ax)
    ax.set_title(f"Distribution des notes pour {course}")
    ax.set_xlabel("Notes")
    ax.set_ylabel("Nombre d'élèves")
    ax.legend()
    canvas.draw()


if __name__ == "__main__":
    if len(sys.argv) != 2 or os.path.isfile(sys.argv[1]) is False:
        print("Wrong arg : expected 'python histogram.py [filename]")
        sys.exit()
    else:
        file = sys.argv[1]

    try :
        data = read_csv_split_houses(file)
    except Exception as e:
        print(f"Erreur while parsing the file {file}")
        sys.exit()

    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.title("Score distribution between houses")

    course_combobox = ttk.Combobox(root, values=list(COURSES))
    course_combobox.set(list(COURSES)[10])
    course_combobox.pack(pady=10)

    fig, ax = plt.subplots(figsize=(8, 6))
    initial_course = list(COURSES)[10]
    ax.clear()
    histogram(data, initial_course, ax)
    ax.set_title(f"Distribution des notes pour {initial_course}")
    ax.set_xlabel("Notes")
    ax.set_ylabel("Nombre d'élèves")
    ax.legend()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()

    course_combobox.bind("<<ComboboxSelected>>", update_plot)

    root.mainloop()
