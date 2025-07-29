
import csv
import traceback
import os
import custom_module
from datetime import datetime

#Task 2: Read a CSV File
def read_employees():
    data = {}
    rows = []

    try:
        with open('../csv/employees.csv', newline='') as csvfile:
            reader= csv.reader(csvfile)
            for i, row in enumerate(reader):
                if i==0:
                    data['fields']= row
                else:
                    rows.append(row)
            data['rows']= rows
            return data
        
    except Exception as e:
         trace_back = traceback.extract_tb(e.__traceback__)
    stack_trace = list()
    for trace in trace_back:
        stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}'
        )
    print(f"Exception type: {type(e).__name__}")
    message = str(e)
    if message:
        print(f"Exception message:{message}")
    print (f"Stack trace: {stack_trace}")
    exit(1)

employees = read_employees()
print(employees)



#Task 3: Find the Column Index
def column_index(column_name):
    return employees['fields'].index(column_name)

employee_id_column = column_index("employee_id")



#Task 4: Find the Employee First Name
def first_name(row_num):
    col_index= column_index("first_name")
    row = employees["rows"][row_num]
    return row[col_index]
print(first_name(0))


#Task 5: Find the Employee: a Function in a Function
def employee_find(employee_id):
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id
    matches=list(filter(employee_match, employees["rows"]))
    return matches
print(employee_find(1))
print(employee_find(3))


#Task 6: Find the Employee with a Lambda
def employee_find_2(employee_id):
    matches= list(filter(lambda row:
        int(row[employee_id_column])== employee_id,
employees["rows"]))
    return matches
print(employee_find_2(1))



#Task 7: Sort the Rows by last_name Using a Lambda
def sort_by_last_name():
    last_name_index = column_index("last_name")
    employees["rows"].sort(key=lambda row:row[last_name_index])
    return employees["rows"]

print(sort_by_last_name())


#Task 8: Create a dict for an Employee
def employee_dict(row):
    headers= employees['fields']
    filtered_headers= headers[1:]
    filtred_values = row[1:]
    return dict(zip(filtered_headers, filtred_values))
print(employee_dict(employees["rows"][1]))



#Task 9: A dict of dicts, for All Employees
def all_employees_dict():
    result ={}
    for row in employees["rows"]:
        employee_id = row[0]
        result[employee_id]= employee_dict(row)
    return result
print(all_employees_dict())



#Task 10: Use the os Module
def get_this_value():
    return os.getenv("THISVALUE")
print(get_this_value())



#Task 11: Creating Your Own Module
def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)
set_that_secret("it is secret")
print(custom_module.secret)



#Task 12: Read minutes1.csv and minutes2.csv
def read_minutes_csv(path):
    with open(path, newline='')as f:
        reader= csv.reader(f)
        fields = next(reader)
        rows = [tuple(row) for row in reader]
        return{ "fields":fields, "rows":rows}
def read_minutes():
    minutes1 = read_minutes_csv("../csv/minutes1.csv")
    minutes2 = read_minutes_csv("../csv/minutes2.csv")
    return minutes1, minutes2
minutes1, minutes2 = read_minutes()
print(read_minutes())



#Task 13: Create minutes_set
def create_minutes_set():
    set1 = set(minutes1["rows"])
    set2 = set(minutes2["rows"])
    return set1.union(set2)
     
minutes_set = create_minutes_set()
print("Combined Minutes Set:")
print(create_minutes_set())


#Task 14: Convert to datetime
def create_minutes_list():
    return list(map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), minutes_set))
minutes_list = create_minutes_list()
print("Minutes List:")
print(minutes_list)



#Task 15: Write Out Sorted List
def write_sorted_list():
    sorted_list = sorted(minutes_list, key=lambda x: x[1])

    converted = list(map(
        lambda x: (x[0], x[1].strftime("%B %d, %Y")),
        sorted_list
    )) 
    with open("minutes.csv", mode="w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(minutes1["fields"]) 
        writer.writerows(converted)      

    return converted
written_minutes = write_sorted_list()
print("Written Minutes:")
print(written_minutes)