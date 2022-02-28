#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 淘宝/天猫秒杀

import datetime
import time

from selenium import webdriver


# 登陆淘宝
def login(browser):
    # 打开淘宝登录页,并进行扫码登录
    browser.get("https://www.taobao.com/")
    time.sleep(3)
    if browser.find_element_by_link_text("亲，请登录"):
        browser.find_element_by_link_text("亲，请登录").click()
        print("请使用手机淘宝扫码登陆,操作限时20s")
        time.sleep(20)
        browser.get(buy_link)
    time.sleep(3)

    now = datetime.datetime.now()
    print('login success:', now.strftime('%Y-%m-%d %H:%M:%S'))

# 秒杀
def spike(buy_time):
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        if now > buy_time:
            webdriver.find_element_by_link_text("立即购买").click()
            break;
        time.sleep(0.1)
    while True:
        try:
            if webdriver.find_element_by_link_text("提交订单"):
                webdriver.find_element_by_link_text("提交订单").click()
        except:
            time.sleep(1)
        print(now)
        time.sleep(0.1)

# main
if __name__ == "__main__":
    # 抢购链接
    # 时间格式："2022-2-28 12:30:00.000000"
    chrome_browser = webdriver.Chrome()  # path形参缺省为环境变量 / 打包为exe后缺省为exe当前目录
    chrome_browser.maximize_window()

    cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    buy_time = input(f"请输入抢购时间, 格式如 {cur_time} :\n")
    buy_link = input("请输入秒杀链接, like: https://detail.tmall.com/item.htm?id=653484370363")

    # 登陆
    login(chrome_browser)
    spike(buy_time,buy_link,chrome_browser)
