import math as m
import time
import libniz
# def lib(i,n):
#     sum=0
#     for j in range(i,n):
#         term=m.pow(-1,j)/(2*j+1)
#         sum+=term
#     return 4*sum
# # print(lib(0,5000))
# # print(lib(5000,10000))

# start_time = time.time()

# print(lib(0,100000000))

# print("--- %s seconds ---" % (time.time() - start_time))

# import time
# import multiprocessing 

# def basic_func(x):
#     if x == 0:
#         return 'zero'
#     elif x%2 == 0:
#         return 'even'
#     else:
#         return 'odd'

# def multiprocessing_func(x):
#     y = x*x
#     # time.sleep(2)
#     print('{} squared results in a/an {} number'.format(x, basic_func(y)))
    
# if __name__ == '__main__':
#     starttime = time.time()
#     processes = []
#     for i in range(0,10000000000000000):
#         p = multiprocessing.Process(target=multiprocessing_func, args=(i,))
#         processes.append(p)
#         p.start()
        
#     print(processes)
#     for process in processes:
#         process.join()
        
#     print('That took {} seconds'.format(time.time() - starttime))

print(libniz.libniz(1000))