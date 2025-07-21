# Task 1: Hello
def hello():
    return "Hello!"
print (hello())


#Task 2: Greet with a Formatted String
name= "James"
def greet(name):
    return f"Hello, {name}!"
print (greet(name))


#Task 3: Calculator
def calc(a,b,operation="multiply"):
     try:
         if operation== "add":
             return a+b
         elif operation == "subtract":
             return a-b
         elif operation == "multiply":
             return a*b
         elif operation == "divide":
             return a/b
         elif operation == "modulo":
             return a%b
         elif operation == "int_divide":
             return a//b
         elif operation =="power":
             return a **b
         else:
             return "Invalid operation"
     except ZeroDivisionError:
         return "You can't divide by 0!"
     except TypeError:
         return "You can't multiply those values!"   
print(calc(5, 0, "divide"))         
print(calc("hello", 2, "multiply"))  
print(calc("hello", "world", "multiply"))  
print(calc(10, 3, "subtract"))     
print(calc(2, 5, "multiply"))          
print(calc(4, 5, "add"))

#Task 4: Data Type Conversion
def data_type_conversion(value, type):
    try:
        if type == "float": 
            return float(value)
        elif type == "int":
            return int(value)
        elif type == "str":
            return str(value)
        else: 
            return f"Invalid data type requested: {type}"
    except (ValueError, TypeError):
        return f"You can't convert {value} into a {type}."
print(data_type_conversion(2,"float"))
print(data_type_conversion("3","float"))
print(data_type_conversion("ab3","int"))
print(data_type_conversion(2,"str"))


#Task 5: Grading System, Using *args
def grade(*args):
    try:
        average = sum(args) / len(args)
        if average >= 90:
            return "A"
        elif average >= 80:
            return "B"
        elif average >= 70:
            return "c"
        elif average >= 60:
            return "D"
        else:
            return "F"
    except (ZeroDivisionError, TypeError):
        return "Invalid data was provided."
print(grade(90,90,85))
print(grade(75,70,85))
print(grade(60,55))
print(grade("hello",55))
print(grade())


#Task 6: Use a For Loop with a Range
def repeat(string,count):
    result =""
    for _ in range(count):
        result += string
    return result
print(repeat("hi", 5))



#Task 7: Student Scores, Using **kwargs
def student_scores(mode, **kwargs):
    try:
        if mode== "best":
            best_student = max(kwargs.items(), key=lambda item: item[1])[0]
            return best_student
        elif mode == "mean":
            average = sum(kwargs.values()) / len(kwargs)
            return average
        else:
            return "Invalid mode"
    except(ValueError, ZeroDivisionError,TypeError):
        return "Invalid data was provided."
print(student_scores("best", Tom=75, Dick=89, Angela=91))
print(student_scores("mean", Tom=75, Dick=89, Angela=91))
print(student_scores("mean")) 


#Task 8: Titleize, with String and List Operations
def titleize(text):
    little_words= {"a", "on", "an", "the", "of", "and","is", "in"}
    words = text.split()
    result=[]
    for i, word in enumerate(words):
        if i == 0 or i == len(words)-1 or word.lower() not in little_words:
            result.append(word.capitalize())
        else:
            result.append(word.lower())

    return " ".join(result)
print(titleize("the lord of the rings")) 



#Task 9: Hangman, with more String Operations
def hangman(secret, guess):
    result = ""
    for letter in secret:
        if letter in guess:
            result+= letter
        else:
            result += "_"
    return result
print(hangman("alphabet", "ab")) 


#Task 10: Pig Latin, Another String Manipulation Exercise
def pig_latin(sentence):
    vowels = "aeiou"
    words = sentence.split()
    result = []

    for word in words:
        if word.startswith("qu"):
            result.append(word[2:]+ "quay")
        elif word[0]in vowels:
            result.append(word + "ay")
        else:
            i=0
            while i < len(word) and word[i] not in vowels:
                if word[i:i+2]== "qu":
                    i +=2
                    break
                i+=1
            result.append(word[i:]+ word[:i]+ "ay")
    return " ".join(result)
print(pig_latin("apple"))                 
print(pig_latin("this is a test"))
print(pig_latin("quiet")) 