# 爬取豆瓣电影排行榜所有类型的电影
import json
import gevent
import random
import requests
import threading
from concurrent.futures import thread, as_completed


def random_str():
    string = 'abcdefghigklmnopqrstuvwxyz'
    ret = ''
    for i in range(10):
        ret += random.choice(string)
    return ret


def worker(count_url, t, id_str):
    agent = random_str()
    headers = {
        'User-Agent': agent,
    }
    response = requests.get(count_url, headers=headers)
    try:
        if response.text:
            total = json.loads(response.text).get('total')
            if total:
                url = 'https://movie.douban.com/j/chart/top_list?type={}&interval_id={}&action=&start=0&limit={}'.format(t, id_str, total)
                movie_list = requests.get(url, headers=headers).json()
                for movie in movie_list:
                    for d in data:
                        if d['url'] == movie['url']:
                            break
                    else:
                        data.append(movie)
                print(url)
    except Exception:
        pass


def task(t):
    agent = random_str()
    headers = {
        'User-Agent': agent,
    }
    gevent_list = []
    for i in range(1, 11):
        id_str = '{}%3A{}'.format(i * 10, (i - 1) * 10)
        count_url = 'https://movie.douban.com/j/chart/top_list_count?type={}&interval_id={}'.format(t, id_str)
        g = gevent.spawn(worker, *(count_url, t, id_str))
        gevent_list.append(g)
    gevent.joinall(gevent_list)
    # return 'OK'
    print('OK')


def main():
    # threading_pool = thread.ThreadPoolExecutor(20)
    threading_list = []
    for t in range(1, 32):
        # th = threading_pool.submit(task, t)
        th = threading.Thread(target=task, args=(t, ))
        threading_list.append(th)
        th.start()

    # for future in as_completed(threading_list):
    #     ret = future.result()
    #     print(ret)
    for th in threading_list:
        th.join()

    new_data = [d for d in data if data.count(d) == 1]

    with open('doubanmovie.txt', mode='w', encoding='utf-8') as fp:
        json.dump(new_data, fp, ensure_ascii=False)
    return new_data


if __name__ == '__main__':
    data = []
    ret = main()
    print(len(ret))  # 21655

