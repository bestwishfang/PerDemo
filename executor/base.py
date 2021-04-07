# -*- coding: utf-8 -*-
import os
import re
import time
import copy
import shutil
from queue import Queue
from threading import Thread

import config


def get_work_path():
    """
    获取工作目录，若不存在并创建
    :return: work_path str
    """
    work_dir = config.WORK_DIR
    work_path = f'{work_dir}/{time.strftime("%Y%m%d%H%M%S")}'
    print(f'work path: {work_path}')
    if not os.path.exists(work_path):
        os.makedirs(work_path)
    return work_path


def get_data(request):
    """
    获取POST请求中json 数据
    :param request:
    :return: data dict
    """
    json_data = request.json
    print("=================================================")
    print(f'json data: \n{type(json_data)}\n{json_data}')
    print("=================================================")
    return json_data


def upload_cases(repository):
    """
    下载或更新测试用例库代码
    :param repository: 测试用例库 ssh git地址
    :return: project_path 用例库在执行机上的路径
    """
    scripts_path = config.SCRIPTS_PATH
    print(f'repository: {repository}')
    project_name = repository.rsplit('/', 1)[1].replace('.git', '')
    project_path = f'{scripts_path}/{project_name}'
    print(f'project_path: {project_path}')
    if os.path.exists(project_path):
        os.chdir(project_path)
        os.system('git pull')
    else:
        os.makedirs(scripts_path)
        os.chdir(scripts_path)
        git_cmd = f'git clone {repository}'
        os.system(git_cmd)
    return project_path


def valid_case(q, case_list, pattern):
    """通过Queue 获取筛选测试用例任务，并处理"""
    while not q.empty():
        pakeage_path = q.get()
        file_list = os.listdir(pakeage_path)
        for file in file_list:
            ret = file.rsplit('.', 1)
            if pattern.match(file):
                if ret[0] not in case_list:
                    file_path = pakeage_path + '/' + file
                    os.remove(file_path)
                else:
                    case_list.remove(ret[0])
        new_file_list = os.listdir(pakeage_path)
        if len(new_file_list) == 2:
            shutil.rmtree(pakeage_path)


def select_cases(cases_path, case_list):
    """
    多线程选取要执行的测试用例，不在任务中删除
    :param cases_path:  测试用例目录
    :param case_list:  测试用例构成的列表
    :return: None
    """
    q = Queue()
    threading_list = []
    pakeages_list = os.listdir(cases_path)
    pattern = re.compile(r'^test_')

    for pakeage in pakeages_list:
        pakeage_path = cases_path + '/' + pakeage
        q.put(pakeage_path)

    for i in range(4):
        t = Thread(target=valid_case, args=(q, case_list, pattern))
        threading_list.append(t)
        t.start()
    for t in threading_list:
        t.join()
    if case_list:
        for case in case_list:
            print(f'TestCases Scripts can not match {case}.')


def exe_cases(cases_path, case_list, frame='pytest'):
    """
    执行机根据task.json 中测试用例进行测试
    :param cases_path:  测试用例目录
    :param case_list:  测试用例构成的列表
    :param frame:  测试工具 默认 pytest
    :return:  None
    """
    original_case_list = copy.deepcopy(case_list)
    print(f'case list: {case_list}\n\noriginal case list: {original_case_list}')
    report_path = f'{cases_path}/../Report'
    pakeages_list = os.listdir(cases_path)
    select_cases(cases_path, case_list)

    for pakeage in pakeages_list:
        pakeage_path = cases_path + '/' + pakeage
        print(f'pakeage_path : {pakeage_path}')
        os.chdir(pakeage_path)
        now_time = time.strftime("%Y%m%d%H%M%S")
        html_path = f'{report_path}/{pakeage}_{now_time}.html'
        if frame == 'pytest':
            exe_cmd = f'pytest --html={html_path}'
            os.system(exe_cmd)
