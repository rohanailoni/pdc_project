import re
from flask import Flask
from celery import Celery
from itsdangerous import json

app = Flask(__name__)
simple_app = Celery('simple_worker', broker='redis://redis:6379/0', backend='redis://redis:6379/0')


@app.route('/start/<fact_id>')
def call_method(fact_id):
    fact=int(fact_id)
    app.logger.info("Invoking Method ")
    #queue name in task folder.function name
    start=0;
    end=fact//2;
    r1 = simple_app.send_task('tasks.longtime_add', kwargs={'start': start,'end':end})
    start=end;
    end=fact
    r2=simple_app.send_task('tasks.longtime_add', kwargs={'start':start ,'end':end});
    app.logger.info(r1.backend)
    dic={'r1':r1.id,'r2':r2.id}
    return json.dumps(dic)


@app.route('/status/<task_id_1>/<task_id_2>')
def get_status(task_id_1,task_id_2):
    status = simple_app.AsyncResult(task_id_1, app=simple_app)
    print("Invoking Method ")
    return "Status of the Task " + str(status.state)


@app.route('/result/<task_id_1>/<task_id_2>')
def task_result(task_id_1,task_id_2):
    r1= simple_app.AsyncResult(task_id_1).result
    r2=simple_app.AsyncResult(task_id_2).result
    result=4*(r1+r2)
    app.logger.info(str(result))
    return "Result of the Task " + str(result)


# if __name__ == '__main__':
  
    
#     app.run()