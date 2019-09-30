import time
from urllib.parse import quote
import bs4
import pymysql
import requests
from pymysql.cursors import DictCursor
import get_city


def connect():
    conn = pymysql.connect(host='localhost', port=3306,
                           database='spider', user='root',
                           password='123456', charset='utf8',
                           autocommit=True,cursorclass = DictCursor
                           )
    return conn


def get_url():
    conn = connect()
    try:
        # 获取游标对象
        with conn.cursor() as cursor:
            # 通过游标执行sql并获取结果
            cursor.execute('SELECT title from tb_zpurl')
            result = cursor.fetchall()
    except pymysql.MySQLError as err:
        # 操作失败回滚事务
        print(err)
    finally:
        # 关闭连接释放资源
        conn.close()
    return result


def main():
    urls = get_url()
    for url in urls[7:]:
        _url = url['title']
        print(_url)
        url = quote(_url)
        for i in range(1, 15):
            url1 = f'https://www.jobui.com/jobs?jobKw={url}&cityKw=%E5%85%A8%E5%9B%BD&n={i}'
            print(i)
            resp = requests.get(
                url = url1,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
                }
            )
            soup = bs4.BeautifulSoup(resp.text, 'lxml')
            work_sort = soup.select('div.c-job-list')
            for sort in work_sort:
                title = sort.select_one('a.job-name').text
                info_url = 'https://www.jobui.com' + sort.select_one('a.job-name')['href']
                conn = connect()
                try:
                    # 获取游标对象
                    with conn.cursor() as cursor:
                        # 通过游标执行sql并获取结果
                        result = cursor.execute(
                            'insert into tb_info_url values (default, %s, %s, %s)', (_url, title, info_url)
                        )
                        if result == 1:
                            conn.commit()
                except pymysql.MySQLError as err:
                    # 操作失败回滚事务
                    print(err)
                finally:
                    # 关闭连接释放资源
                    conn.close()
                print(info_url)
            time.sleep(0.5)


if __name__ == '__main__':
    main()