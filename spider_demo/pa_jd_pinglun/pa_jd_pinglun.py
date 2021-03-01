import os
import requests
import time
import random
import jieba
import matplotlib.pyplot as plt
from fake_useragent import UserAgent
from wordcloud import WordCloud, ImageColorGenerator


def get_response(user_agent, proxy_list, product_id, page):
    url = 'https://sclub.jd.com/comment/productPageComments.action'
    data = {
        'productId': product_id,
        'score': '0',
        'sortType': '5',
        'page': page,
        'pageSize': '10',
        'isShadowSku': '0',
        'rid': '0',
        'fold': '1',
    }
    headers = {
        'Referer': 'https://item.jd.com/{}.html'.format(product_id),
        # 'User-Agent': user_agent.random,
        'User-Agent': user_agent,
    }
    # 使用代理
    # proxies = {
    #     'http': 'http://{}'.format(random.choice(proxy_list)),
    #     'https': 'https://{}'.format(random.choice(proxy_list)),
    # }
    # try:
    #     response = requests.get(url, params=data, proxies=proxies, headers=headers, timeout=5)
    #     return response.json()
    # except Exception as err:
    #     get_response(user_agent, proxy_list, product_id, page)

    response = requests.get(url, params=data, headers=headers)
    return response.json()


def spider_jd_comments(user_agent):
    product_id = 50704019883  # 商品id
    file_path = '{}_comments.txt'.format(product_id)
    if os.path.exists(file_path):
        os.remove(file_path)
    # 使用代理
    proxy_list = []
    # for i in range(20):
    #     proxy = requests.get('http://127.0.0.1:5555/random').text
    #     if proxy not in proxy_list:
    #         proxy_list.append(proxy)

    # 爬取前10页评论
    for page in range(10):
        ret = get_response(user_agent, proxy_list, product_id, page)
        content_list = ret['comments']
        with open(file_path, mode='a', encoding='utf-8') as fp:
            for content in content_list:
                fp.write(content['content'].strip() + '\n')
                print(content['content'].strip())
        time.sleep(random.random() * 3)

    return file_path


def get_content(file_path):
    # 加载文本 并分词
    content = ''
    with open(file_path, mode='r', encoding='utf-8') as fp:
        for line in fp.readlines():
            if line.strip():
                # jieba 精确模式
                seg = jieba.cut(line, cut_all=False)
                content += ' '.join(seg)
    return content


def build_word_cloud(content):
    # 加载背景图
    background_image = plt.imread('./wawa.jpg')
    # 生成词云对象
    cloud = WordCloud(
        background_color='white',
        mask=background_image,
        font_path='./simhei.ttf'
    )
    # 生成词云文本
    word_cloud = cloud.generate(content)
    # 提取背景图的颜色，来设置词云文本的颜色
    color = ImageColorGenerator(background_image)

    # 重新设置 词云文本的颜色
    cloud.recolor(color_func=color)
    return word_cloud


def show_cloud(file_path):
    content = get_content(file_path)
    word_cloud = build_word_cloud(content)
    # plt.imshow(word_cloud, interpolation="bilinear")
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()


def main():
    # user_agent = UserAgent()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    file_path = spider_jd_comments(user_agent)
    # 生成词云, 展示
    show_cloud(file_path)


if __name__ == '__main__':
    main()
