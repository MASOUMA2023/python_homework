#Task 3: List Comprehensions Practice
import csv 

with open ("../csv/employees.csv", newline='') as file:
    reader = csv.reader(file)
    data = list(reader)

full_names = [row[0]+ ' '+ row[1] for row in data[1:]]
print("All employee names:", full_names)
names_with_e = [name for name in full_names if 'e' in name.lower()]
print("Names containing 'e':", names_with_e)