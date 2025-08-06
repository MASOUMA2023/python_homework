#Task 1: Introduction to Pandas - Creating and Manipulating DataFrames
import pandas as pd
import json
import numpy as np
import os
print("Current working directory:", os.getcwd())


data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}
task1_data_frame = pd.DataFrame(data)
print('step1: task1_data_frame')
print(task1_data_frame)

task1_with_salary = task1_data_frame.copy()
task1_with_salary['Salary']= [70000, 80000, 90000]
print('\nstep2: task1_with_salary')
print(task1_with_salary)

task1_older = task1_with_salary.copy()
task1_older["Age"]= task1_older["Age"]+1
print('\nstep3: task1_older')
print(task1_older)

task1_older.to_csv('employees.csv', index=False)
print("\nStep 4: DataFrame added to CSV file 'employees.csv'")


#Task 2: Loading Data from CSV and JSON
task2_employees = pd.read_csv('employees.csv')
print("task2_employees DataFrame from CSV:")
print(task2_employees)

additional_employees_data = [
    {"Name": "Eve", "Age": 28, "City": "Miami", "Salary": 60000},
    {"Name": "Frank", "Age": 40, "City": "Seattle", "Salary": 95000}
]
with open('additional_employees.json', 'w') as f:
    json.dump(additional_employees_data, f, indent=4)

json_employees = pd.read_json('additional_employees.json')
print("\njson_employees DataFrame loaded from JSON:")
print(json_employees)

more_employees = pd.concat([task2_employees, json_employees], ignore_index=True)
print("\nmore_employees combined DataFrame:")
print(more_employees)


#Task 3: Data Inspection - Using Head, Tail, and Info Methods
first_three = more_employees.head(3)
print("\nfirst_three (first 3 rows):")
print(first_three)

last_two = more_employees.tail(2)
print("\nlast_two (last 2 rows):")
print(last_two)

employee_shape = more_employees.shape
print("\nemployee_shape (rows, columns):")
print(employee_shape)

print("\nDataFrame info:")
more_employees.info()



#Task 4: Data Cleaning
dirty_data = pd.read_csv("dirty_data.csv")
print("Original dirty_data:")
print(dirty_data)

clean_data = dirty_data.copy()

clean_data = clean_data.drop_duplicates()
print("\nAfter removing duplicates:")
print(clean_data)

clean_data['Age'] = pd.to_numeric(clean_data['Age'], errors='coerce')
print("\nAfter converting Age to numeric:")
print(clean_data)

clean_data['Salary'] = pd.to_numeric(
    clean_data['Salary'].replace(['unknown', 'n/a'], np.nan),
    errors='coerce'
)
print("\nAfter converting Salary to numeric:")
print(clean_data)

clean_data['Age'] = clean_data['Age'].fillna(clean_data['Age'].mean())
clean_data['Salary'] = clean_data['Salary'].fillna(clean_data['Salary'].median())
print("\nAfter filling missing Age and Salary:")
print(clean_data)

clean_data['Hire Date'] = pd.to_datetime(clean_data['Hire Date'], errors='coerce')
clean_data['Hire Date'] = clean_data['Hire Date'].fillna(pd.Timestamp("2000-01-01"))
print("\nAfter converting Hire Date to datetime:")
print(clean_data)

clean_data['Name'] = clean_data['Name'].str.strip().str.upper()
clean_data['Department'] = clean_data['Department'].str.strip().str.upper()
print("\nAfter cleaning Name and Department columns:")
print(clean_data)
