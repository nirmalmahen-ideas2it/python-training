new_list=["abc","def","aba","1221"]

result_list=list(filter(lambda x:(len(x)>2 and x[0] is x[-1]), new_list))
print(result_list)