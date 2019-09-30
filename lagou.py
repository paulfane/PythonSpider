"""爬取拉勾网数据"""
import pickle
import random
import threading
import time

import requests

import get_city, get_job
from concurrent.futures.thread import ThreadPoolExecutor
import pymysql
from urllib.parse import quote
from selenium import webdriver


def get_conn():
    """"获取数据库连接"""
    return pymysql.connect(host="localhost", port=3306, database="spider",
                           user="root", password="123456", charset="utf8", autocommit=True)


def ensure_conn():
    thread_local = threading.local()
    if not getattr(thread_local, "conn", None):
        setattr(thread_local, "conn", get_conn())
    return thread_local.conn


def save_data(data):
    try:
        with ensure_conn().cursor() as cursor:
            cursor.execute("insert into tb_job(language, company, salary, advantage, info) values(%s, %s, %s, %s, %s)", data[0])
    except pymysql.MySQLError as err:
        print(err)


def get_data(jobs_url):
    urls = []
    # 设置无头浏览器参数
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    # 启动无头浏览器
    driver = webdriver.Chrome(options=options)
    driver.get(jobs_url)
    page = 1
    try:
        total_page = driver.find_element_by_css_selector(
            "#order > li > div.item.page > div.page-number > span.span.totalNum").text
    except:
        total_page = "0"
    print(type(total_page))
    while page <= int(total_page):
        print(f"第{page}页")
        try:
            url_boxs = driver.find_elements_by_css_selector(
                "#s_position_list > ul > li div.list_item_top > div.position > div.p_top > a ")
            print(len(url_boxs))
            for url in url_boxs:
                print(url.get_attribute("href"))
                urls.append(url.get_attribute("href"))
            print("find_next")
            page += 1
            new_url = f"{jobs_url}{page}/"
            print(new_url)
            driver.get(new_url)
            print("find_next_ok")
        except:
            break
    driver.quit()
    print("退")
    return urls


def operation_data(url):
    pass


def get_urls(keyword=""):
    pass


def get_headless_chrome():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    # 启动无头浏览器
    driver = webdriver.Chrome(options=options)
    return driver


def save_url_cities(cities, jobs):
    try:
        with open('cities.txt', 'wb') as file_stream:
            file_stream.write(pickle.dumps(cities, ))
        with open('jobs.txt', 'wb') as file_stream:
            file_stream.write(pickle.dumps(jobs))
    except:
        pass


def save_url_db(urls):
    try:
        tmp = tuple()
        for url in urls:
            tmp += (url, )
        with ensure_conn().cursor() as cursor:
            cursor.executemany("insert into tb_href(no, href) values(default, %s)", tmp)
    except pymysql.MySQLError as err:
        print(err)


def main():
    # cities = get_city.get_cities()
    driver = get_headless_chrome()
    jobs = get_job.get_jobs(driver)
    urls = []
    for url in jobs:
        urls += get_data(url)
        if len(urls) >= 60:
            save_url_db(urls)
            urls.clear()
        time.sleep(random.randint(3, 5))


if __name__ == '__main__':
    main()


