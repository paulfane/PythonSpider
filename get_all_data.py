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
            cursor.execute("insert into tb_data(job_position, job_company, job_salary, job_address, job_info, job_advantage) values(%s, %s, %s, %s, %s, %s)", data[0])
    except pymysql.MySQLError as err:
        print(err)


def del_db_urls(table, urls):
    tuple_urls = tuple(urls)
    try:
        with ensure_conn().cursor() as cursor:
            sql = f"delete from {table} where href = %s"
            cursor.executemany(sql, tuple_urls)
    except pymysql.MySQLError as err:
        print(err)


def get_data(url):
    time.sleep(random.randint(2, 4))
    data = []
    headers = {
        "Host": "www.lagou.com",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Accept": "*/*",
        "Referer": "https://www.lagou.com/jobs/5808482.html",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "user_trace_token=20190621170255-d5ab6466-c9c7-4e1f-b9fa-9ce1cf5603b3; _ga=GA1.2.1474711451.1561107776; LGUID=20190621170256-5c12c311-9403-11e9-a441-5254005c3644; _gid=GA1.2.1620476166.1562584481; index_location_city=%E5%8C%97%E4%BA%AC; LG_HAS_LOGIN=1; hasDeliver=0; privacyPolicyPopup=false; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216bd15244a732e-04194d5a9d6d9f-e343166-1327104-16bd15244a8327%22%2C%22%24device_id%22%3A%2216bd15244a732e-04194d5a9d6d9f-e343166-1327104-16bd15244a8327%22%2C%22props%22%3A%7B%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2275.0.3770.100%22%2C%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; JSESSIONID=ABAAABAABEEAAJAD43E6048B4BA416BD1E141B88F72F26C; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1562659944,1562668806,1562720966,1562745493; LGSID=20190710155813-77b1fac0-a2e8-11e9-be22-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F6079182.html; LG_LOGIN_USER_ID=a997e4ee2fbf538fc4c11f2abbf61f7fd05b825c30525b3166bb72febd32e197; _putrc=4E8210DF149F6DF4123F89F2B170EADC; login=true; unick=%E5%B0%8F%E5%8C%85; gate_login_token=fcc2c8f8e7a86e5de6b2e050c77c35319840515a6065954f8c82a5899ae062da; _gat=1; TG-TRACK-CODE=index_navigation; SEARCH_ID=a3a2ef1da30e49c68e7c6545614c16a3; X_HTTP_TOKEN=e774173ca4a1767948954726518d247977dc2e069a; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1562745984; LGRID=20190710160624-9c408b1a-a2e9-11e9-a4de-5254005c3644"
    }
    resp = requests.get(url=url, headers=headers)
    soup = bs4.BeautifulSoup(resp.text, "lxml")
    print(soup.prettify())
    # job_position
    keyword = soup.select_one("body > div.position-head > div > div.position-content-l > div")
    # job_info, job_advantage
    print(keyword["title"])
    # job_company
    company = soup.select_one("#job_company > dt > a > div > h3 > em")
    # job_salary
    salary = soup.select_one("body > div.position-head > div > div.position-content-l > dd > h3 > span.salary")
    print(salary.text)
    # job_address
    address = soup.select_one("body > div.position-head > div > div.position-content-l > dd > h3 > span:nth-child(2)")
    print(address.text)
    # job_info
    infos = soup.select("#job_detail > dd.job_bt > div > p")
    description = ""
    for info in infos:
        description += info.text
    advantage = soup.select_one("#job_detail > dd.job-advantage")
    data.append((keyword["title"], clear_data(company.text), salary.text, clear_data(address.text), clear_data(description), clear_data(advantage.text)))
    return data


def operation_data(url):
    data = get_data(url)
    save_data(data)


def main():
    used_urls = []
    try:
        with ThreadPoolExecutor(max_workers=16) as pool:
            for page in range(0, 16000, 1000):
                urls = get_db_urls("tb_href", page, 1000)
                for url in urls:
                    pool.submit(operation_data, url)
    except:
        print("err")
        pass
    finally:
        del_db_urls("tb_href", used_urls)


if __name__ == '__main__':
    main()