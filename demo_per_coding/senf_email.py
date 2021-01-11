# 定时任务和邮件发送

import smtplib
from email.mime.text import MIMEText


# send email
def send_email():
    # 接受方邮箱地址
    receivers = ['bestwishfang@foxmail.com']
    # 发送方邮箱地址
    msg_from = 'bestwishfang@126.com'
    password = 'continue00'  # 邮箱授权码
    # 邮件内容
    # 主题
    subject = "TestCrontab"
    # 正文
    content = "This is a test demo."

    # 使用MIMEText对文本信息进行封装
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['Form'] = msg_from
    msg['To'] = ','.join(receivers)
    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.126.com')
        smtp.login(msg_from, password)
        smtp.sendmail(msg_from, receivers, msg.as_string())
        print("发送成功")
        smtp.close()
    except Exception as err:
        print(err)
        print("发送失败")


if __name__ == '__main__':
    send_email()




import pymongo
import smtplib
from redis import Redis
from email.mime.text import MIMEText

r = Redis(host='10.10.14.245', port=6379)
client = pymongo.MongoClient(host='10.10.14.245', port=27017)


def total_task():
    value = r.get('count')
    return int(value)


# 未爬取任务数量
def unfinish_task():
    value = r.lrange('taoche:start_urls', 0, -1)
    return len(value)


def data_count():
    db = client['NewSC']
    ret = db['cars'].find()
    return len(list(ret))


def send_email(content):
    # 接受方邮箱地址
    receivers = ['bestwishfang@foxmail.com']
    # 发送方邮箱地址
    msg_from = 'bestwishfang@126.com'
    passwd = 'continue00'  # 邮箱授权码
    # 邮件内容
    # 主题
    subject = "TestCron"
    # 正文
    content = content

    # 使用 MIMEText 对文本信息进行封装
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['Form'] = msg_from
    msg['To'] = ','.join(receivers)
    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.126.com')
        smtp.login(msg_from, passwd)
        smtp.sendmail(msg_from, receivers, msg.as_string())
        print("发送成功")
        smtp.close()
    except Exception as err:
        print(err)
        print("发送失败")


if __name__ == '__main__':
    # 总任务数
    total = total_task()
    res1 = "总的任务数：{}".format(total)
    print(res1)
    unfinish = unfinish_task()
    finish = total - unfinish
    res2 = "已完成任务数：{}".format(finish)
    print(res2)

    rate = round(finish / total * 100, 2)
    res3 = "任务完成进度：{}%".format(rate)
    print(res3)

    nums = data_count()
    res4 = "当前已爬取到的数据总量：{}".format(nums)
    print(res4)

    content = '\n'.join([res1, res2, res3, res4])
    send_email(content)

