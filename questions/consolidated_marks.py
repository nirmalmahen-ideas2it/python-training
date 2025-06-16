from collections import defaultdict

marks_Tuple=[('Alice', 90), ('Bob', 85), ('Alice', 95)]

marks_dict = defaultdict(int)  # Initialize with int as default factory

for tup in marks_Tuple:
    marks_dict[tup[0]] += tup[1]

print(marks_dict)
