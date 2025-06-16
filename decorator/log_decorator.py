import time 
def log_decorator(func):
    def wrapper(*args, **kwargs):
         startTime=time.time()
         result=func(*args, **kwargs)
         endTime=time.time()
         print(f"The time taken for function: {func.__name__} is {endTime-startTime:.5f} seconds")
         return result
    return wrapper

@log_decorator
def addition(x,y):
     time.sleep(3)
     return x+y;

if __name__ == "__main__":
    addition(5,10)