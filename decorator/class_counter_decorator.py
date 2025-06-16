from typing import Any

class Counter:
    def __init__(self, func):
        self.func=func
        self.count=0

    def __call__(self, *args, **kwds) :
        self.count+=1
        print(f"The function {self.func.__name__} is executed {self.count} times")
        return self.func(*args, **kwds)

@Counter
def sayHi():
    print("Hi!")

for i in range (3):
    sayHi()