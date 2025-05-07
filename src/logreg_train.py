import csv
from global_variable import courses, houses
import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def read_csv(filepath):
    data = {}
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for house in houses:
            data[house] = {}
        for row in reader:
            # Pour chaque clé, transformer la valeur en float ou None
            for key, value in row.items():
                if key in courses:
                    try:
                        row[key] = float(value) if value != '' else float("NaN")
                    except ValueError:
                        row[key] = float("NaN")
                if key not in data[row["Hogwarts House"]]:
                    data[row["Hogwarts House"]][key] = []
                data[row["Hogwarts House"]][key].append(row[key])
    return data

file = "./src/datasets/dataset_train.csv"
data = read_csv(file) # to do adjust values

thetas = []
for course in courses:
    currentTheta = [0]
    for house in houses:
        currentTheta.add(0) #create 1 theta per course
    thetas.append(currentTheta)

student_house = []
student_grades = {}
for house, student in data:
    if house == "Gryffindor":
        student_house.add([1,0,0,0])
    if house == "Ravenclaw":
        student_house.add([0,1,0,0])
    if house == "Slytherin":
        student_house.add([0,0,1,0])
    if house == "Hufflepuff":
        student_house.add([0,0,0,1])
    student_grades[student["Index"]] = {}
    for course, grade in student:
        if course not in courses:
            continue
        student_grades[student["Index"]][course] = grade #=> voir pour la normalise

