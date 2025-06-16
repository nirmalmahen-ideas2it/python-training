import random
def retry(func):
    def wrapper(*args, **kwargs):
        for attempt in range(1,4):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"The following error {e.__cause__} occured during attempt {attempt} of {func.__name__} call")
        print("All attempts failed")
    return wrapper
    
@retry
def randomFunc():
    if random.choice([True, False]) :
        raise ValueError("Random Failure")
    return "Success"
print(randomFunc())