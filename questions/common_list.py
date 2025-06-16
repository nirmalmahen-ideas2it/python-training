arr_1=[1,2,3,4,5,6]
arr_2=[2,4,6,1]
common_arr=[]
for num in arr_1:
    if num in arr_2:
        common_arr.append(num)

print(common_arr)

common_arr2=[ x for x in arr_1 if x in arr_2]
print(f"Common List: {common_arr2}")