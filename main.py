import matplotlib.pyplot as plt
import math
import numpy as np
import xlrd
import openpyxl as op
import pandas as pd

input_type = int(input("Enter 1 for manual input, 2 for text file input, and 3 for excel data input \n"))
if input_type == 1:
    x_array = []
    y_array = []
    C_array = []
    explanatory = input("What is the explanatory variable: ")
    response = input("What is the response variable: ")
    num_points = int(input("Enter the number of data points: "))
    print("Enter the values for " + explanatory + ": ")
    for i in range(0, num_points):
        element1 = float(input())
        x_array.append(element1)
        C_array.append(1)  # weight for a (the y-intercept) is always 1
        C_array.append(element1)  # weights for b (the slope) is the given values for the explanatory variable
    print("Enter the values for " + response + ": ")
    for i in range(0, num_points):
        element2 = float(input())
        y_array.append(element2)
    y_array = np.reshape(y_array, (num_points, 1))  # constructing a nx1 matrix for the y-values
    C_array = np.reshape(C_array, (num_points, 2))  # constructing a nx2 matrix for the C-matrix
    C_transpose = np.transpose(C_array)
    operation1 = np.matmul(C_transpose, C_array)
    operation2 = np.linalg.inv(operation1)
    operation3 = np.matmul(operation2, C_transpose)
    operation4 = np.matmul(operation3, y_array)
    a = operation4[0][0]
    b = operation4[1][0]
else:
    if input_type == 2:
        file_name = input("What is the name of the text file you are working with? \n")
        grade_info = pd.read_csv(file_name)
    elif input_type == 3:
        file_name = input("What is the name of the excel file you are working with? \n")
        grade_info = pd.read_excel(file_name)
    explanatory = grade_info.columns[0]
    response = grade_info.columns[1]
    x_array = grade_info[grade_info.columns[0]]
    x_numpy = x_array.to_numpy()
    num_points = len(x_array)
    x_reshaped = np.reshape(x_numpy, (num_points, 1))
    y_array = grade_info[grade_info.columns[1]].to_numpy()
    append_ones = np.ones((num_points, 1))
    C_array = np.hstack((append_ones, x_reshaped))
    #operations on C
    C_transpose = np.transpose(C_array)
    operation1 = np.matmul(C_transpose, C_array)
    operation2 = np.linalg.inv(operation1)
    operation3 = np.matmul(operation2, C_transpose)
    operation4 = np.matmul(operation3, y_array)
    a = operation4[0]
    b = operation4[1]

print("The data set can be modeled by: y = " + str(a) + " + " + str(b) + "x")

# standard deviation calculator
total_x = 0
for r in x_array:
    total_x += r
mean_x = total_x / num_points
distance_total_x = 0
for r in x_array:
    distance_total_x += (mean_x - r) ** 2
variance_x = distance_total_x / (num_points - 1)
sd_x = math.sqrt(variance_x)
total_y = 0
for r in y_array:
    total_y += r
mean_y = total_y / num_points
distance_total_y = 0
for r in y_array:
    distance_total_y += (mean_y - r) ** 2
variance_y = distance_total_y / (num_points - 1)
sd_y = math.sqrt(variance_y)

correlation_coefficient = (b * sd_x) / sd_y
print("The correlation coefficient is " + str(correlation_coefficient))
if correlation_coefficient > 0.8 or correlation_coefficient < -0.8:
    print("The model can effectively predict the changes in the response variable")
elif correlation_coefficient > 0.5 or correlation_coefficient < -0.5:
    print("The model is moderately effective in predicting the changes in the response variable")
else:
    print("The model is not very effective in predicting the changes in the response variable")
print("\n")

# graphing
min_x = x_array[0]
for r in x_array:
    if r < min_x:
        min_x = r
max_x = x_array[0]
for r in x_array:
    if r > max_x:
        max_x = r

plt.scatter(x_array, y_array)
x_range = np.linspace(0, max_x, 100)
y = b * x_range + a
plt.xlabel(explanatory)
plt.ylabel(response)
plt.plot(x_range, y)
plt.grid()
plt.show()
