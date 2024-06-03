import requests

url = 'http://106.39.42.196:9990/query'
data = {'msg': '机器学习这门课程中讲了蒙特卡洛方法。'}
response = requests.post(url, json=data)
print(response.json())