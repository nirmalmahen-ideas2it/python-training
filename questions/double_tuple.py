list_tuples=[(1,2),(2,4),(4,5)]

double_tuple= [(x[0]*2, x[1]*2) for x in list_tuples]
# print(double_tuple)

swap_tuple= [(x[1],x[0]) for x in list_tuples]

# print(swap_tuple)

tup_1=(1,2,2)
print(set(tup_1))
tup_2=(2,3)

tup_3= tuple(tup_1+tup_2)
print(tup_3)