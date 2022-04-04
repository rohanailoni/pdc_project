

cdef double libniz(int i,int n):
    cdef double sum=0.0
    cdef double term=0.0
    for j in range(i,n):
        term=(-1**j)/(2*j+1)
        sum=sum+term
    return 4*sum
