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
