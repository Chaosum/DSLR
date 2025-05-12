import os
import sys
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from constants.global_variable import COURSES
from utils.plot_utils import read_csv_split_houses, scatter_plot


def on_closing():
    root.destroy()
    sys.exit(0)


def update_plot(event=None):
    feature1 = course_combobox1.get()
    feature2 = course_combobox2.get()

    if feature1 == feature2:
        error_label.config(text="Les deux matières doivent être différentes.")
        return
    error_label.config(text="")

    ax.clear()
    scatter_plot(data, feature1, feature2, ax)
    ax.set_title(f"{feature1} vs {feature2}")
    ax.set_xlabel(feature1)
    ax.set_ylabel(feature2)
    ax.legend()
    canvas.draw()


def validate_selection(event):
    update_plot()


def load_data():
    if len(sys.argv) > 2:
        print("Usage: python describe.py [optional: filename]")
        sys.exit(1)
    if len(sys.argv) == 2 and os.path.isfile(sys.argv[1]):
        return read_csv_split_houses(sys.argv[1])
    print("Using default file: ./src/datasets/dataset_train.csv")
    return read_csv_split_houses("./src/datasets/dataset_train.csv")


if __name__ == "__main__":
    data = load_data()

    root = tk.Tk()
    root.title("Features Similarity")
    root.protocol("WM_DELETE_WINDOW", on_closing)

    error_label = tk.Label(root, text="", fg="red")
    error_label.pack()

    # Combobox 1
    course_combobox1 = ttk.Combobox(root, values=COURSES, state="readonly")
    course_combobox1.set(COURSES[0])
    course_combobox1.pack(pady=10)
    course_combobox1.bind("<<ComboboxSelected>>", validate_selection)

    # Combobox 2
    course_combobox2 = ttk.Combobox(root, values=COURSES, state="readonly")
    course_combobox2.set(COURSES[1])
    course_combobox2.pack(pady=10)
    course_combobox2.bind("<<ComboboxSelected>>", validate_selection)

    fig, ax = plt.subplots(figsize=(8, 6))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()

    update_plot()

    root.mainloop()
