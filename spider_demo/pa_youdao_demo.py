import time
import random
import hashlib
import requests


def random_str():
    string = 'abcdefghigklmnopqrstuvwxyz'
    ret = ''
    for i in range(10):
        ret += random.choice(string)
    return ret


def create_md5(string):
    md5 = hashlib.md5()
    md5.update(bytes(string, encoding='utf-8'))
    ret = md5.hexdigest()
    return ret


url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

i = input("请输入要翻译的词：").strip()

ts = str(int(time.time() * 1000))
salt = ts + str(random.randint(0, 9))
string = "fanyideskweb" + i + salt + "n%A-rKaT5fb[Gy?;N5@Tj"
sign = create_md5(string)

agent = random_str()
bv = create_md5(agent)

form_data = {
    'i': i,
    'from': 'AUTO',
    'to': 'AUTO',
    'smartresult': 'dict',
    'client': 'fanyideskweb',
    'salt': salt,
    'sign': sign,
    'ts': ts,
    'bv': bv,
    'doctype': 'json',
    'version': '2.1',
    'keyfrom': 'fanyi.web',
    'action': 'FY_BY_REALTlME',
}
headers ={
    # 'Accept': 'application/json, text/javascript, */*; q=0.01',
    # 'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Connection': 'keep-alive',
    'Content-Length': str(233 + len(i)),
    # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'OUTFOX_SEARCH_USER_ID_NCOO=493197149.3625508; OUTFOX_SEARCH_USER_ID="-1133926341@10.169.0.81"; _ga=GA1.2.1727849886.1564042546; _ntes_nnid=2beb1a7491f35300f20c2ead37829737,1566630056963; JSESSIONID=aaaGx477-PdfDbvvXAC3w; ___rl__test__cookies=1571380847796',
    # 'Host': 'fanyi.youdao.com',
    # 'Origin': 'http://fanyi.youdao.com',
    'Referer': 'http://fanyi.youdao.com/',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'User-Agent': agent,
    # 'X-Requested-With': 'XMLHttpRequest',
}

response = requests.post(url, form_data, headers=headers)
print(response.text)

"""
Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
Content-Length: 236
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: OUTFOX_SEARCH_USER_ID_NCOO=493197149.3625508; OUTFOX_SEARCH_USER_ID="-1133926341@10.169.0.81"; _ga=GA1.2.1727849886.1564042546; _ntes_nnid=2beb1a7491f35300f20c2ead37829737,1566630056963; JSESSIONID=aaaGx477-PdfDbvvXAC3w; ___rl__test__cookies=1571380847796
Host: fanyi.youdao.com
Origin: http://fanyi.youdao.com
Referer: http://fanyi.youdao.com/
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36
X-Requested-With: XMLHttpRequest
"""