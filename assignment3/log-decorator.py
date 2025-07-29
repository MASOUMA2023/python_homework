#Task 1: Writing and Testing a Decorator
import  logging
from functools import wraps

logger= logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger. addHandler(logging.FileHandler("./decorator.log", "a"))
def logger_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        pos_args = list(args) if args else "none"
        kw_args = dict(kwargs) if kwargs else "none"
        log_message= (
         f"function: {func.__name__} "
            f"positional parameters: {pos_args} "
            f"keyword parameters: {kw_args} "
            f"return: {result}"
        )
        logger.info(log_message)
        return result
    return wrapper
@logger_decorator
def greet():
    print("Hello, World!")

@logger_decorator
def check_args(*args):
    return True
@logger_decorator
def return_decorator(**kwargs):
    return logger_decorator

if __name__ == "__main__":
    greet()
    check_args(1,2,3)
    return_decorator(a=10, b=20)    





