#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os

"""
仿真环境配置管理口脚本

前提条件：
1、Linux执行机username: root, password: root
2、Linux执行机python 已安装，版本 3.5+，pip 正常使用
3、Linux执行机ssh 公钥和私钥已生成，且是3072位，公钥路径：/root/.ssh/id_rsa.pub

备注：
ssh 密钥生成命令 ssh-keygen -t rsa -b 3072
"""

import_flag = True
while import_flag:
    try:
        import pytest
        import pytest_testlib_base
    except ImportError as err:
        print('err:', err)
        print('err name：', err.name)
        if err.name == 'pytest_testlib_base':
            os.system('pip install pytest-testlib-base -i http://10.247.195.169/simple/')
        else:
            os.system('pip install {} -i http://cmc-cd-mirror.rnd.huawei.com/pypi/simple/'.format(err.name))
    else:
        import_flag = False

if __name__ == '__main__':
    pytest_fp = os.popen('find / -name pytest')
    pytest_path = pytest_fp.readline()
    if '/usr/' in pytest_path and '/pytest' in pytest_path:
        pytest_path = pytest_path.strip('\n')
        exe_cmd = '{} {}'.format(pytest_path, __file__)
        os.system(exe_cmd)
else:
    import re
    import time
    from pytest_testlib_base import Log
    from pytest_testlib_base.SSHConnect import SSHConnection


def load_pub_key():
    with open('/root/.ssh/id_rsa.pub', mode='r', encoding='utf-8') as fp:
        pub_key = fp.read().strip()
    return pub_key


def get_process_pid(ne, procname):
    rs = ne.sendcmd("ps axf | grep -a %s | grep -v grep | grep -v systemctl | grep -v stop" % procname,
                    endflags=("#",), timeout=5)
    pid = re.findall(r'\s+(\d+)\s+\S+', rs)
    if pid:
        pid = pid[0]
    return pid


def kill_process(ne, proc_name=None, sig_type=None, proc_id=None):
    if proc_name:
        pid = get_process_pid(ne, proc_name)
    else:
        pid = proc_id
    if sig_type:
        ne.sendcmd("kill -%d %s" % (sig_type, pid), endflags=("#",), timeout=20)
    else:
        ne.sendcmd("kill %s" % pid, endflags=("#",), timeout=20)


def link_v8(ne):
    rs = ne.sendcmd("docker ps").split("\n")
    for line in rs:
        if "mpu" in line:
            ret = ne.sendcmd("ifconfig docker0")
            res = re.findall(r'broadcast\s+(\d+\.\d+\.\d+\.\d+)\s+', ret)
            if res:
                ip_num_list = res[0].rsplit('.', 1)
                ip_num_list[1] = str(int(ip_num_list[1]) - 1)
                master_ip = '.'.join(ip_num_list)

                ne.sendcmd('rm -f /root/.ssh/known_hosts')
                ne.sendcmd(f"ssh -o StrictHostKeyChecking=no {master_ip}", endflags=("assword:", "#"), confirm="root")
                kill_process(ne, "time_client_start", sig_type=9)
                time.sleep(20)
                ne.sendcmd('/opt/workdir/bin/time_client_start', endflags=('<HUAWEI>',), timeout=20)
                return master_ip


def set_mange_port(ne):
    time.sleep(1)
    pub_key = load_pub_key()
    cmd_list = [
        'sys',
        'rsa peer-public-key abcd encoding-type openssh',
        'p b',
        pub_key,
        'p e',
        'p e',
        'user-interface vty 4',
        'authentication-mode aaa',
        'protocol inbound all',
        'user privilege level 3',
        'quit',
        'ssh ipv4 server port 15000',
        'ssh ipv6 server port 15000',
        'ssh user root',
        'ssh user root authentication-type rsa',
        'ssh user root assign rsa-key abcd',
        'ssh user root service-type all',
        'ssh authorization-type default root',
        'ssh client first-time enable',
        'ssh server publickey dsa ecc rsa rsa_sha2_256 rsa_sha2_512',
        'stelnet server enable',
        'snetconf server enable',
        'commit',
        'ssh server-source all-interface',
    ]
    pattern = re.compile(r'Warning(.*?)ontinue.*?\[Y/N\]:')
    for cmd in cmd_list:
        ret = ne.sendcmd(cmd, endflags=(']', '[Y/N]:'), timeout=20)
        if pattern.findall(ret):
            ne.sendcmd('Y', endflags=(']', '[Y/N]:'), timeout=20)


def test_set_manage_port():
    fp = os.popen('ifconfig eth0', 'r')
    ip_pattern = re.compile(r'inet (\d+\.\d+\.\d+\.\d+)\s')
    ifconfig_eth0 = fp.read()
    executor_ip = ip_pattern.findall(ifconfig_eth0)[0]
    ne = SSHConnection(name='every',
                       ip=executor_ip,
                       username='root',
                       password='root')
    ne.login()
    time.sleep(1)
    master_ip = link_v8(ne)
    set_mange_port(ne)
    try:
        ne.relogin()
        cmd = f'ssh -o StrictHostKeyChecking=no {master_ip} -p 15000'
        ret = ne.sendcmd(cmd, endflags=('<HUAWEI>',), timeout=20)
    except Exception as err:
        Log.log(err)
        assert False, err
    else:
        assert '<HUAWEI>' in ret
        Log.log('Set device mange port OK!')
    finally:
        ne.logout()
