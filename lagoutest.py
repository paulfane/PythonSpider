import random
import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor
from urllib.parse import quote

import pymysql
from selenium import webdriver
import get_job, get_city


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


def get_data(url):
    data = []
    driver = webdriver.Chrome()
    driver.get(url)
    salary = driver.find_element_by_css_selector("body > div.position-head > div > div.position-content-l > dd > h3 > span.salary")
    print(salary.text)
    keyword = driver.find_element_by_css_selector("body > div.position-head > div > div.position-content-l > div")
    print(keyword.get_attribute("title"))
    company = driver.find_element_by_css_selector("#job_company > dt > a > div > h3 > em")
    advantage = driver.find_element_by_css_selector("#job_detail > dd.job-advantage")
    infos = driver.find_elements_by_css_selector("#job_detail > dd.job_bt > div > p")
    description = ""
    for info in infos:
        description += info.text
    data.append((keyword.get_attribute("title"), company.text, salary.text, advantage.text, description))
    driver.quit()
    return data


def operation_data(url):
    data = get_data(url)
    save_data(data)


def get_urls(url):
    urls = []
    print(url)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    # 启动无头浏览器
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    # chengdu = driver.find_element_by_css_selector("#changeCityBox > ul > li:nth-child(7) > a")
    # chengdu.click()
    # search = driver.find_element_by_css_selector("#search_input")
    # search.send_keys(keyword)
    # submit = driver.find_element_by_css_selector("#search_button")
    # submit.click()
    page = 0
    while page < 15:
        print(f"第{page + 1}页")
        try:
            url_boxs = driver.find_elements_by_css_selector("#s_position_list > ul > li div.list_item_top > div.position > div.p_top > a ")
            for url in url_boxs:
                urls.append(url.get_attribute("href"))
            print("find_next")
            next = driver.find_element_by_css_selector('#s_position_list > div.item_con_pager > div > a:nth-child(7)')
            print("find_next_ok")
            webdriver.ActionChains(driver).move_to_element(next).click(next).perform()
            print("find_next_click")
            page += 1
        except:
            break
    driver.quit()
    print("退")
    return urls


def get_headless_chrome():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    # 启动无头浏览器
    driver = webdriver.Chrome(options=options)
    return driver


def main():
    driver = get_headless_chrome()
    jobs = get_job.get_jobs(driver)
    urls = []
    for url in jobs:
        print("getget")
        urls += (get_urls(url))
        time.sleep(random.randint(3, 5))
    for url in urls:
        print(url)
    # for url in urls:
    #     with ThreadPoolExecutor(max_workers=16) as pool:
    #         pool.submit(operation_data, url)


if __name__ == '__main__':
    main()
