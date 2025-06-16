import random

def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Calling function {func.__name__}")
        result=func(*args, **kwargs)
        print(f"End of function call {func.__name__}")
        return result
    return wrapper

def has_Access(role):
    def decorator(func):
        def wrapper(*args,**kwargs):
            if (role == "ADMIN"):
                print("Authorized")
                return func(*args,**kwargs)
            else:
                print("Unauthorized")
                raise ValueError("UnAuthorized Access")
        return wrapper
    return decorator

def retry_method(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for time in range(0,times):
                try: 
                    return func(*args, **kwargs)
                except ValueError as e:
                    print(f"Failure: {e.__cause__}, Going to retry- {time}")
                 
        return wrapper
    return decorator        

def closure_func(power):
    def calc(num):
        return num**power
    return calc

sqaure=closure_func(2)

@has_Access(role="ADMIN")
@retry_method(3)
@logger
def calculate_sqaure(num):
        if random.choice([True,False]):
            return sqaure(num)
        else:
            raise ValueError("Run time Exception")

result= calculate_sqaure(5)
print(result)