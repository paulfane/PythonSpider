import bs4
import pymysql
import requests
from lagou import ensure_conn


def get_urls():
    urls = set()
    resp = requests.get("https://jobs.51job.com/")
    soup = bs4.BeautifulSoup(resp.text, "lxml")
    hrefs = []
    for i in range(2, 5):
        hrefs += soup.select(f"body > div.maincenter > div:nth-child(3) > div:nth-child({i}) a")
    for href in hrefs:
        urls.add(href["href"])
    print(urls)
    return urls


def save_to_db(urls):
    try:
        with ensure_conn().cursor() as cursor:
            cursor.executemany("insert into tb_51(no, href) value(default, %s)", tuple(urls))
    except pymysql.MySQLError as err:
        print(err)


def main():
    urls = get_urls()
    save_to_db(urls)


if __name__ == '__main__':
    main()