from log_decorator import log_decorator

def call_counter(func):
    counter=0
    def wrapper(*args, **kwargs):
        nonlocal counter
        counter+=1
        print(f"Function {func.__name__} is executed {counter} times")
        return func(*args, **kwargs);
    return wrapper

@call_counter
@log_decorator
def greetName(name):
    print (f"Hello {name}")

@call_counter
def greet():
    print ("Hello!")

for i in range(1,5):
    greet()

for i in range(1,3):
    greetName("Alice")

for i in range(1,3):
    greet()