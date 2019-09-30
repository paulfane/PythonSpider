import random
import threading
import time
from urllib.parse import quote
import get_city
import bs4
import pymysql
import requests
from pymysql.cursors import DictCursor


def get_kw():
    kws = []
    resp = requests.get(url="https://www.jobui.com/",
                 headers={
                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
                     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                     'Accept-Encoding': 'gzip, deflate, br',
                     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
                 }
                 )
    soup = bs4.BeautifulSoup(resp.text, 'lxml')
    hrefs = soup.select("body > div.astruct.cfix > div > div.employer-box > div > div:nth-child(1) > div:nth-child(6) a")
    for href in hrefs:
        print(href.text)
        kws.append(href.text)
    return kws


def get_urls(cities, kws):
    info_urls = set()
    for kw in kws:
        for city in cities:
            for index in range(1, 50):
                url = f"https://www.jobui.com/jobs?jobKw={quote(kw)}&cityKw={quote(city)}&n={index}"
                print(url)
                resp = requests.get(
                    url=url,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
                    }
                )
                soup = bs4.BeautifulSoup(resp.text, 'lxml')
                try:
                    job_sort = soup.select('div.c-job-list')
                    print(len(job_sort))
                    if len(job_sort) == 0:
                        break
                    for sort in job_sort:
                        info_url = 'https://www.jobui.com' + sort.select_one('a.job-name')['href']
                        print(info_url)
                        info_urls.add(info_url)
                except:
                    print("开始下一轮")
                    break
            print(len(info_urls))
            time.sleep(random.randint(2, 4))
        print(len(job_sort))
        # 前端工程师未曾爬取并保存
        save_url_db(list(info_urls))
        del_db_kw(kw)
        info_urls.clear()
    print(len(job_sort))
    return list(info_urls)


def get_conn():
    """"获取数据库连接"""
    return pymysql.connect(host="localhost", port=3306, database="spider",
                           user="root", password="123456", charset="utf8", autocommit=True)


def ensure_conn():
    thread_local = threading.local()
    if not getattr(thread_local, "conn", None):
        setattr(thread_local, "conn", get_conn())
    return thread_local.conn


def save_url_db(urls):
    try:
        tmp = tuple()
        for url in urls:
            tmp += (url, )
        with ensure_conn().cursor() as cursor:
            cursor.executemany("insert into tb_zhiyouji(no, href) values(default, %s)", tmp)
    except pymysql.MySQLError as err:
        print(err)


def del_db_kw(kw):
    try:
        with ensure_conn().cursor() as cursor:
            cursor.execute("delete from tb_kw where kw = %s", (kw, ))
    except pymysql.MySQLError as err:
        print(err)


def get_kw_from_db():
    kws = []
    try:
        with ensure_conn().cursor() as cursor:
            cursor.execute("select kw from tb_kw where no >= 4")
            for tmp in cursor.fetchall():
                kws.append(tmp[0])
    except pymysql.MySQLError as err:
        print(err)
    print(kws)
    return kws


def main():
    kws = get_kw_from_db()
    cities = get_city.get_cities()
    cities.remove("全国")
    print(cities)
    get_urls(cities, kws)


if __name__ == '__main__':
    main()