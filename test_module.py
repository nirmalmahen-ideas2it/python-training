# print(f"The value of __name__ in test_module.py is: {__name__}")

# # Importing main.py as a module
# import main

# # Using the greet function
# message = main.greet("Alice")
# print(message)  # Output: Hello, Alice!

# # Using the calculate_sum function
# result = main.calculate_sum(10, 20)
# print(f"10 + 20 = {result}")  # Output: 10 + 20 = 30

# # We can still call main() if we want to
# print("\nCalling main() function:")
# main.main()

numsList=list(map(lambda x: x*2, range(1,6)))
print(numsList)

numsListTwo=list(filter(lambda x: (x**0.5).is_integer(), range(1,31)))
print(numsListTwo)

words = ['cat', 'apple', 'banana', 'dog', 'elephant']
words=list(filter(lambda x: len(x)>3,words))
print(words)

pairs = [(1, 3), (4, 1), (5, 2), (2, 4)]
pairsNew=list(sorted(pairs, key=lambda x:x[1], reverse=True))
print(pairsNew)    

obbCubes=list(map(lambda x:((x**3)%2!=0), range(1,16)))
print(obbCubes)






# We can also access other functions or variables from main.py
# For example, if main.py had a function called calculate():
# result = main.calculate() 