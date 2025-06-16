
def fibo():
    n1=0
    n2=1
    count=0
    while(True):
        if count==0:
            yield n1
        elif count==1:
            yield n2
        elif count>1:
            n3=n1+n2
            n1=n2
            n2=n3
            yield n3
        count+=1
        

result=fibo()
for num in range(10):
    print(next(result))
