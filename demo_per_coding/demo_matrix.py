#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

try:
    import re
    import os
    import argparse
    import subprocess
    import shutil
    import docker
    from pymongo import MongoClient
    import yaml
except ImportError as e:
    if e.name == "yaml":
        e.name = "pyyaml"
    print("""依赖包{}未安装; 请使用以下命令安装:
          python3 -m pip install -i http://rnd-mirrors.huawei.com/pypi/simple/  --trusted-host rnd-mirrors.huawei.com {}""".format(e.name, e.name))
    exit(-1)


def check_file_arg(file_ext):
    class Act(argparse.Action):
        def __call__(self, parser, namespace, fname, option_string=None):
            if not os.path.exists(fname):
                parser.error('{} not exist'.format(fname))
            ext = os.path.splitext(fname)[1][1:]
            if ext != file_ext:
                option_string = '({})'.format(option_string) if option_string else ''
                parser.error("file doesn't end with one of {}{}".format(file_ext, option_string))
            else:
                setattr(namespace, self.dest, fname)

    return Act


def get_args():
    # parent_parser = argparse.ArgumentParser(add_help=False)
    # parent_parser.add_argument('action',
    #                     help='action for env',
    #                     choices=['start', 'stop'])

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='action for env')
    # 添加子命令 add
    parser_start = subparsers.add_parser('start', help='start matrix env')
    parser_start.add_argument('cc_file',
                            help='first startup cc fullname',
                            action=check_file_arg('cc'))
    parser_start.add_argument('topo_file',
                        help='topo fullname of ne',
                        action=check_file_arg('yaml'))
    parser_start.set_defaults(func=do_matrix_start)

    # 添加子命令 sub
    parser_stop = subparsers.add_parser('stop', help='stop matrix env')
    parser_stop.set_defaults(func=do_matrix_stop)
    args = parser.parse_args()
    return args


def system(cmd_list):
    '''
    执行命令行
    :param cmd_list: 列表格式['ifconfig','eth0']
    :return: str
    '''
    return bytes.decode(subprocess.Popen(cmd_list, stdout=subprocess.PIPE).stdout.read())


def get_container_ip(container_name, dev='eth0'):
    rs = system(['docker', 'exec', container_name, 'sh', '-c', 'ifconfig {}'.format(dev)])
    ip = re.findall(r'inet addr:(\d+.\d+.\d+.\d+)', rs, re.MULTILINE)[0]
    return ip


def set_first_start_cc(cc_name):
    '''
    将首次启动的cc包全路径写到ne_volume目录的配置文件中，用于后面rtmd容器启动时准备cc包和注入启动环境变量
    :param cc_name:
    :return:
    '''
    work_dir = os.path.realpath('./')
    cfg_file = '{}/ne_volume/first_startup_cc.cfg'.format(work_dir)
    with open(cfg_file, mode='w') as fd:
        fd.write(cc_name)


def create_testbed(topofile):
    rtmdIpInfo = os.popen("docker exec rtmd ip addr show eth0 | grep inet").read()
    iplist = rtmdIpInfo.split()
    ip = (iplist[1].split('/'))[0]
    rtmd_data = {'name': 'name', 'type': 'linux', 'protocol': 'ssh', 'ip': ip, 'username': 'root', 'password': 'root'}
    os.system("cp "+topofile+" ./testbed.yaml")
    with open(topofile, encoding='utf-8') as fd:
        topo_content = yaml.load(fd.read(), Loader=yaml.FullLoader)
    topo_content['testbedinfo']['devices']['dta']['boards']['rtmd'] = rtmd_data
    with open("testbed.yaml", 'w') as fw:
        yaml.dump(topo_content, fw)


def do_matrix_start(args):
    '''
    matrix命令行的start子命令执行函数
    :param args:
    :return:
    '''
    image = '100.95.233.94/simulator/matrix:latest'
    work_dir = os.path.realpath('./')
    container_name = 'rtmd'
    volumes = ['-v', '/sys/fs/cgroup:/sys/fs/cgroup:ro',
               '-v', '/var/run/docker.sock:/docker.sock',
               '-v', '{}/cfg_templates:/cfg_templates'.format(work_dir),
               '-v', '{}/ne_volume:/ne_volume'.format(work_dir)
               #'-v', '/usr1/common_volume/matrix_attach_files:/opt/workdir/bin'
               ]
    run_rtmd_cmdlist = ['docker', 'run', '-d',
                        '--privileged',
                        '--name', container_name,
                        '--hostname', container_name,
                        '--network', 'bridge',
                        '--cap-add=ALL'
                        ] + volumes + [image]

    ne_root = '{}/ne_volume'.format(work_dir)
    try:
        os.makedirs(ne_root)
    except OSError as e:
        print(e)
        shutil.rmtree(ne_root)
        return
    cc_filename = os.path.basename(args.cc_file)
    shutil.copy(os.path.realpath(args.cc_file), ne_root)
    shutil.copy(os.path.realpath(args.topo_file), '{}/topo.yaml'.format(ne_root))
    # system(['ln', '-s', os.path.realpath(args.cc_file), '{}/{}'.format(ne_root, cc_filename)])
    set_first_start_cc(cc_filename)
    rs = system(run_rtmd_cmdlist)
    print(rs)
    # 如果创建rtmd容器失败则删除ne_volume目录
    if 'Error' in rs:
        shutil.rmtree(ne_root)
        return
    create_testbed(args.topo_file)


def do_matrix_stop(args):
    '''
    matrix命令行的stop子命令执行函数
    :param args:
    :return:
    '''
    work_dir = os.path.realpath('./')
    ne_volume = '{}/ne_volume'.format(work_dir)
    docker_client = docker.from_env()
    try:
        rtmd_ip = get_container_ip('rtmd')
        mongo_client = MongoClient(rtmd_ip, 27017)
        for board_info in mongo_client.deploy.board.find():
            board_container = docker_client.containers.get(board_info['board_name'])
            try:
                board_container.remove(force=True)
            except docker.errors.APIError as e:
                # 如果由于容器内部的文件被加保护导致无法删除容器，需要将容器内部加保护的文件去保护
                host_fs_path = re.findall(r'failed to remove root filesystem: unlinkat (\S+)/diff', e.explanation)[0]
                os.system('find {}/diff | xargs chattr -i'.format(host_fs_path))
                board_container.remove(force=True)
            mongo_client.deploy.board.remove({'_id': board_info['_id']})
    except Exception as e:
        print(e)
        container_names = []
        if os.path.exists(ne_volume):
            files = os.listdir(ne_volume)
            for file in files:
                fullpath = os.path.join(ne_volume, file)
                if (os.path.isdir(fullpath)):
                    container_names.append(file)
        for container_name in container_names:
            system(['docker', 'rm', '-f', container_name])

    os.system("losetup  | grep 'cc (deleted)' | awk '{print $1}' | grep '/dev/loop' | xargs losetup -d")
    os.system('docker rm -f rtmd')
    os.system('docker network rm ns')
    os.system('find {}/ne_volume | xargs chattr -i'.format(work_dir))
    shutil.rmtree('{}/ne_volume'.format(work_dir), ignore_errors=True)
    os.system('rm testbed.yaml')


if __name__ == '__main__':
    args = get_args()
    args.func(args)
