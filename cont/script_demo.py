import time
from selenium import webdriver

chrome = webdriver.Chrome()

# url = 'https://www.baidu.com/'
# chrome.get(url)
#
# chrome.find_element_by_id('kw').send_keys('Python就业')
# chrome.find_element_by_id('su').click()


url = 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?proxy_url=https%3A//qzs.qq.com/qzone/v6/portal/proxy.html&daid=5&&hide_title_bar=1&low_login=0&qlogin_auto_login=1&no_verifyimg=1&link_target=blank&appid=549000912&style=22&target=self&s_url=https%3A%2F%2Fqzs.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&pt_qr_app=手机QQ空间&pt_qr_link=https%3A//z.qzone.com/download.html&self_regurl=https%3A//qzs.qq.com/qzone/v6/reg/index.html&pt_qr_help_link=https%3A//z.qzone.com/download.html&pt_no_auth=0'

# url = 'https://user.qzone.qq.com/917453305/infocenter?via=toolbar'
chrome.get(url)
chrome.find_element_by_id('').click()

# time.sleep(20)
# chrome.close()

time.sleep(10)

print("选择个人中心")
chrome.find_element_by_id('aIcenter').click()

# time.sleep(15)
# print("选择说说框")
#
# chrome.find_element_by_id('$1_substitutor_content').send_keys(" New Start From Script ...")
#
# time.sleep(5)
# print("发表说说")
# chrome.find_element_by_xpath('//*[@id="QM_Mood_Poster_Inner"]/div/div[4]/div[4]/a[2]').click()


time.sleep(15)
print("签到")
chrome.find_element_by_id('checkin_button').click()


