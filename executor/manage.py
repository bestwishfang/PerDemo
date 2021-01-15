# -*- coding: utf-8 -*-
import os
import json
import shutil

import base

from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/exe_cases/', methods=['POST', 'GET'])
def exe_cases():
    if request.method == 'POST':
        print('\n********************In exe_cases method post********************\n')
        work_path = base.get_work_path()
        json_data = base.get_data(request)
        task_file = f'{work_path}/task.json'
        with open(task_file, mode='w', encoding='utf-8') as fp:
            json.dump(json_data, fp, ensure_ascii=False, indent=4)

        # 从用例库下载用例，并拷贝到工作目录下
        repository = json_data.get('repository')
        project_path = base.upload_cases(repository)
        script_path = f'{work_path}/scripts'
        shutil.copytree(project_path, script_path)

        # 执行测试用例
        cases_path = f'{script_path}/cases'
        cases_dict = json_data.get('cases')
        case_list = list(cases_dict.keys())
        frame = json_data.get('frame')
        base.exe_cases(cases_path, case_list, frame)

        return 'Executor Cases'
    else:
        return 'Request Method is not Right!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug='True')
