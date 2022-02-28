# -*- coding:utf-8 -*-
"""
Author：SPIDERMAN
Time: 2021/7/19
Software: PyCharm
"""
import json
from concurrent import futures
from urllib.parse import quote, unquote

import requests
from bs4 import BeautifulSoup as bs

"""
百度图片https://image.baidu.com/
360搜图：https://image.so.com/
微软：https://cn.bing.com/images/trending?FORM=ILPTRD
"""




def baidu_get_image_url(keywords, max_number=10000, use_proxy=None):
    """
    获取百度图片urls
    :param keywords: 关键词
    :param max_number: 获取图片数量
    :param use_proxy: 是否使用代理
    :return:
    """
    def decode_url(url):
        in_table = '0123456789abcdefghijklmnopqrstuvw'
        out_table = '7dgjmoru140852vsnkheb963wtqplifca'
        translate_table = str.maketrans(in_table, out_table)
        mapping = {'_z2C$q': ':', '_z&e3B': '.', 'AzdH3F': '/'}
        for k, v in mapping.items():
            url = url.replace(k, v)
        return url.translate(translate_table)

    base_url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592" \
               "&lm=7&fp=result&ie=utf-8&oe=utf-8&st=-1&face=0"
    keywords_str = "&word={}&queryWord={}".format(
        quote(keywords), quote(keywords))
    query_url = base_url + keywords_str

    init_url = query_url + "&pn=0&rn=30"
    proxies = None
    # if use_proxy:
    #     proxies = {"http": "{}://{}".format(proxy_type, proxy),
    #                "https": "{}://{}".format(proxy_type, proxy)}

    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    response = requests.get(init_url, proxies=proxies, headers=headers)
    init_json = json.loads(response.text)
    # 全部图片数量
    total_num = init_json['listNum']
    print("目标网站搜索结果为:{}".format(total_num ))
    crawl_num = min(max_number, total_num)
    # 一页60个图片 接口一次30条

    crawled_urls = list()
    # 请求一次30条
    batch_size = 30

    with futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_list = list()

        def get_image_urls(page, batch_size):
            image_urls = list()
            url = query_url + "&pn={}&rn={}".format(page * batch_size, batch_size)
            try_time = 0
            while True:
                try:
                    response = requests.get(url, proxies=proxies, headers=headers)
                    break
                except Exception as e:
                    try_time += 1
                    if try_time > 3:
                        print(e)
                        return image_urls
            response.encoding = 'utf-8'
            res_json = json.loads(response.text)
            for data in res_json['data']:
                if 'objURL' in data.keys():
                    image_urls.append(decode_url(data['objURL']))
                elif 'replaceUrl' in data.keys() and len(data['replaceUrl']) == 2:
                    image_urls.append(data['replaceUrl'][1]['ObjURL'])

            return image_urls

        for page in range(0, int((crawl_num + batch_size - 1) / batch_size)):
            future_list.append(executor.submit(get_image_urls, page, batch_size))
        for future in futures.as_completed(future_list):
            if future.exception() is None:
                crawled_urls += future.result()
            else:
                print(future.exception())
    crawled_urls = list(set(crawled_urls))
    return crawled_urls[:min(len(crawled_urls), crawl_num)]

def bing_get_image_url(keywords, max_number=10000, use_proxy=None):
    """
    获取必应图片urls
    :param keywords: 关键词
    :param max_number: 获取图片数量
    :param use_proxy: 是否使用代理
    :return:
    """
    crawled_urls = list()
    def find_image_url(html):
        image_urls = list()
        soup = bs(html, 'lxml')
        image_elements = soup.find_all('a',attrs='iusc')
        for image_element in image_elements:
            m_json_str = image_element["m"]
            m_json = json.loads(m_json_str)
            image_urls.append(m_json["murl"])
        return image_urls
    base_url = "https://cn.bing.com/images/async?count=35&cw=1689&ch=249&relp=35&tsc=ImageBasicHover&datsrc=I&layout=RowBased_Landscape&mmasync=1&dgState=x*0_y*0_h*0_c*7_i*36_r*5&IG=9921BE4B40B941CB8078BE6F1F74599B&iid=images.5544"
    keywords_str = "&q={}".format(quote(keywords))
    query_url = base_url + keywords_str
    proxies = None
    # if use_proxy:
    #     proxies = {"http": "{}://{}".format(proxy_type, proxy),
    #                "https": "{}://{}".format(proxy_type, proxy)}

    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    # 请求一次35条
    batch_size = 35
    with futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_list = list()
        def get_image_urls(page, batch_size):
            image_urls = list()
            url = query_url + "&first={}&SFX={}".format(page * batch_size, page)
            try_time = 0
            while True:
                try:
                    response = requests.get(url, proxies=proxies, headers=headers)
                    break
                except Exception as e:
                    try_time += 1
                    if try_time > 3:
                        print(e)
                        return image_urls
            first_data = find_image_url(response.text)
            image_urls += first_data
            return image_urls

        for page in range(0, int((max_number+batch_size) / batch_size)+1):
            future_list.append(executor.submit(get_image_urls, page, batch_size))
        for future in futures.as_completed(future_list):
            if future.exception() is None:
                crawled_urls += future.result()
            else:
                print(future.exception())
    crawled_urls = list(set(crawled_urls))
    return crawled_urls[:min(len(crawled_urls), max_number)]

def i360_get_image_url(keywords, max_number=10000, use_proxy=None):
    """
    获取360图片urls
    :param keywords: 关键词
    :param max_number: 获取图片数量
    :param use_proxy: 是否使用代理
    :return:
    """
    base_url = "https://image.so.com/j?pd=1&pn=60&correct=%E4%B8%AD%E5%9B%BD%E5%9C%B0%E5%9B%BE&adstar=0&tab=all&sid=3d5cb4d00501224658973509860cbfc4&ras=0&cn=0&gn=0&kn=50&crn=0&bxn=20&cuben=0&pornn=0&manun=50&src=srp"
    keywords_str = "&q={}".format(quote(keywords))
    query_url = base_url + keywords_str
    init_url = query_url + "&sn=0"
    proxies = None
    # if use_proxy:
    #     proxies = {"http": "{}://{}".format(proxy_type, proxy),
    #                "https": "{}://{}".format(proxy_type, proxy)}

    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    response = requests.get(init_url, proxies=proxies, headers=headers)
    init_json = json.loads(response.text)
    # 全部图片数量
    total_num = init_json['total']
    print("目标网站搜索结果为:{}".format(total_num ))
    # 一页60个图片 接口一次30条
    crawl_num = min(max_number, total_num)
    crawled_urls = list()
    # 请求一次30条
    batch_size = 50
    with futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_list = list()
        def get_image_urls(page, batch_size):
            image_urls = list()
            url = query_url + "&sn={}".format(page * 10)
            try_time = 0
            while True:
                try:
                    response = requests.get(url, proxies=proxies, headers=headers)
                    break
                except Exception as e:
                    try_time += 1
                    if try_time > 3:
                        print(e)
                        return image_urls
            response.encoding = 'utf-8'
            res_json = json.loads(response.text)
            for data in res_json['list']:
                image_urls.append(data['img'])
            return image_urls
        for page in range(0, int((crawl_num + batch_size - 1) / batch_size)):
            future_list.append(executor.submit(get_image_urls, page, batch_size))
        for future in futures.as_completed(future_list):
            if future.exception() is None:
                crawled_urls += future.result()
            else:
                print(future.exception())
    crawled_urls = list(set(crawled_urls))
    return crawled_urls[:min(len(crawled_urls), crawl_num)]

def crawl_image_urls(keywords, engine="baidu", max_number=10000,use_proxy=False):
    """
    :param keywords:
    :param engine:
    :param max_number:
    :param use_proxy:
    :return:
    """
    print("目标网站为:{}".format(engine))
    print("关键词为:  " + keywords)
    if max_number <= 0:
        print("目标抓取不能为0")
        max_number = 10000
    else:
        print("抓取数量为:{}条".format(max_number))
    image_urls = 0
    if engine== "baidu":
        image_urls = baidu_get_image_url(keywords, max_number=max_number,use_proxy=use_proxy)
    elif engine == "bing":
        image_urls = bing_get_image_url(keywords, max_number=max_number, use_proxy=use_proxy)
    elif engine == "360":
        image_urls = i360_get_image_url(keywords, max_number=max_number, use_proxy=use_proxy)
    else:   # Baidu
        print('目前只支持baidu、360、bing')
    if len(image_urls)>=0:
        print("目标抓取:{0}条 已抓取:{1}条".format(max_number, len(image_urls)))
    else:
        print("抓取异常".format(max_number, len(image_urls)))


    return image_urls

if __name__ == '__main__':
    res = i360_get_image_url('中国地图',100)
    # res = baidu_get_image_url('中国地图',100)
    # res = bing_get_image_url('中国地图',100)

    print(res)
    print(len(res))
    print(len(set(res)))
