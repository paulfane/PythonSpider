import threading
import time

import pymysql

import test_zhiyouji


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
            cursor.executemany("insert into tb_kw(no, kw) values(default, %s)", tmp)
    except pymysql.MySQLError as err:
        print(err)


kws = test_zhiyouji.get_kw()
save_url_db(kws)
