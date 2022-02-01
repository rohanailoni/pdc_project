import math as m
import time
def lib(i,n):
    sum=0
    for j in range(i,n):
        term=m.pow(-1,j)/(2*j+1)
        sum+=term
    return 4*sum
# print(lib(0,5000))
# print(lib(5000,10000))

start_time = time.time()

print(lib(0,100000000))

print("--- %s seconds ---" % (time.time() - start_time))
