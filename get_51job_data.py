import random
import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor
import bs4
import pymysql
import re
import requests
from selenium import webdriver
from lagou import ensure_conn


def clear_data(content):
    return re.sub(r"[\s【】\n\t\/]+", "", content)


def get_db_urls(table, min, max):
    urls = []
    try:
        with ensure_conn().cursor() as cursor:
            sql = f"select href from {table} limit %s, %s"
            cursor.execute(sql, (min, max))
            for href in cursor.fetchall():
                urls.append(href[0])
    except pymysql.MySQLError as err:
        print(err)
    print(urls)
    return urls


def save_data(data):
    try:
        with ensure_conn().cursor() as cursor:
            cursor.executemany("insert into tb_data(job_position, job_company, job_salary, job_address, job_info) values(%s, %s, %s, %s, %s)", data)
    except pymysql.MySQLError as err:
        # 应该pass掉
        pass


def get_data(url):
    data = []
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    resp = requests.get(url=url, headers=headers)
    soup = bs4.BeautifulSoup(resp.text, "lxml")
    total_page = soup.select_one("#cppageno > span:nth-child(2)")
    pattern = re.compile(r"[\u4e00-\u9fa5](?P<total>[0-9]*)[\u4e00-\u9fa5]，[\u4e00-\u9fa5]+")
    anchor_list = pattern.findall(total_page.text)
    total = int(anchor_list[0])
    for page in range(1, total):
        new_url = f"{url}p{page}/"
        print(new_url)
        resp = requests.get(url=new_url, headers=headers)
        soup = bs4.BeautifulSoup(resp.text, "lxml")
        jobs = soup.select("div.detlist.gbox > div.e")
        if len(jobs) == 0:
            break
        for job in jobs:
            # job_position
            job_positons = job.select_one("p.info > span.title > a")
            print(job_positons.text)
            # job_company
            company = job.select_one("p.info > a")
            print(company.text)
            # job_salary
            salary = job.select_one("p.info > span:nth-child(4)")
            print(salary.text)
            # job_address
            address = job.select_one("p.info > span.location.name")
            print(address.text)
            # job_info
            infos = job.select_one("p.text")
            description = infos.text
            # advantage = soup.select_one("#job_detail > dd.job-advantage")
            tmp =(clear_data(job_positons.text), clear_data(company.text), salary.text, clear_data(address.text), clear_data(description))
            data.append(tmp)
        if len(data) >= 500:
            save_data(data)
            data.clear()
    return data


def operation_data(url):
    data = get_data(url)
    save_data(data)
    return 1


def save_page(page):
    with open("page.txt", "w") as file_stream:
        file_stream.write(str(page))


def main():
    urls = get_db_urls("tb_51", 0, 1000)
    urls = urls[25:]
    with ThreadPoolExecutor(max_workers=10) as pool:
        for index, url in enumerate(urls):
            pool.submit(operation_data, url)
            save_page(index)


if __name__ == '__main__':
    main()