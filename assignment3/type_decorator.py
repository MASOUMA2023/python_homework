#Task 2: A Decorator that Takes an Argument
from functools import wraps

def type_convertor(type_of_output):
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            x = func(*args, **kwargs)
            return type_of_output(x)
        return wrapper
    return decorator

@type_convertor(str)
def return_int():
    return 5

@type_convertor(int)
def return_string():
    return "not a number"

if __name__ == "__main__":
    y= return_int()
    print(type(y).__name__)

    try:
        y = return_string()
        print("shouldn't get here!")
    except ValueError:
        print("can't convert that string to an integer!")




