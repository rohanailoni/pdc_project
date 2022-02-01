import requests



response = requests.get('http://172.19.0.3:5000/simple_start_task/11')
print(response.json()['r1'])
