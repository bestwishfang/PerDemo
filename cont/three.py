"""
print("use ssh id_rsa...")

print("modify in fang")
"""
import paramiko

ssh = paramiko.SSHClient()
know_hosts = paramiko.AutoAddPolicy()
ssh.set_missing_host_key_policy(know_hosts)

ssh.connect(
    hostname="10.10.14.245",
    port=22,
    username="fang",
    password="123456",
)

# 实例化一个terminal
shell = ssh.invoke_shell()
shell.settimeout(1)  # 命令执行的等待时间

command = input("[fang@localhost~]$") + "\n"
shell.send(command)

while True:
    try:
        recv = shell.recv(1024).decode()
        if recv:
            print(recv, end='')
        else:
            continue
    except:
        command = input("") + "\n"
        if command.strip('\n') == 'exit':
            break
        else:
            shell.send(command)
"""
after exit debug
"""
