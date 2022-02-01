import imp
import time
from celery import Celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

def factorial(x):
    if x==1 or x==0:
        return 1;
    else:
        return x*factorial(x-1)
import math as m
def lib(i,n):
    sum=0
    for j in range(i,n):
        term=m.pow(-1,j)/(2*j+1)
        sum+=term
    return sum



@app.task()
def longtime_add(start,end):
    logger.info('Got    Request - Starting work ')
    ans=lib(start,end)
    logger.info("start"+str(start)+"end"+str(end))
    logger.info('Work Finished ')
    return ans
