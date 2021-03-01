# 给flask项目添加数据

import requests

line_list = []
send_data = {}
url = 'http://127.0.0.1:5000/api/buyer'

with open('class_info.csv', mode='rb') as f:
    for line in f:
        line_list.append(line.decode('utf-8'))
    line_list = line_list[1:]
    for new_line in line_list:
        send_data['class_num'], send_data['class_name'], send_data['entrance_time'], send_data['college'] = \
        [l.strip() for l in new_line.split(',')]
        print(send_data)
        ret = requests.post(url, data=send_data)
        print(ret.json())

