"""
前十职位地区分布情况
"""
import draw_top10jobs_address
import pymysql
from collections import Counter

kws = [
    {
        'java': 'Java开发工程师'
    }, {
        'c': 'C语言开发工程师'
    }, {
        '前端': 'web前端开发工程师'
    }, {
        '运维': '运维工程师'
    }, {
        '测试': '测试工程师'
    }, {
        '推广': '网络推广专员'
    }, {
        '美工': '美工设计师'
    }, {
        '新媒体运营': '新媒体运营专员'
    }, {
        '游戏开发': '游戏开发工程师'
    }, {
        'c++': 'c++开发工程师'
    }, {
        '运营专员': '网络运营专员'
    }]


def get_connect():
    return pymysql.connect(host="localhost", port=3306, database="spider",
                           user="root", password="123456", charset="utf8", autocommit=True)


def get_all_data(sql):
    conn = get_connect()
    list = []
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            for job in cursor.fetchall():
                list.append(job[0])
    except pymysql.MySQLError:
        conn.rollback()
    finally:
        conn.close()
        return list


def get_address(top_10):
    data = []
    for kw in top_10:
        address_list = get_all_data(f"select job_address from tb_data where job_position like '%{kw}%'")
        data.append(address_list)
    return data


def top_10_job(job_list):
    jobs = []
    for kw in kws:
        for job in job_list:
            key = list(kw)[0]
            if key in job.lower():
                jobs.append(kw[key])
                job_list.remove(job)
    jobs = jobs + job_list
    top_10 = Counter(jobs).most_common(10)
    return top_10


def get_keys(top_10):
    keys = []
    values = []
    for item in top_10:
        keys.append(item[0])
        values.append(item[1] * 5)
    return (keys, values)


def get_new_kws(kvs):
    new_kws = []
    for kw in kws:
        new_kw = list(kw)[0]
        print(kw[new_kw])
        for kv in kvs[0]:
            if new_kw in kv.lower():
                new_kws.append(new_kw)
                kvs[0].remove(kw[new_kw])
    new_kws = new_kws + kvs[0]
    return new_kws


def get_useful_data(top_10, data):
    new_data1 = []
    new_data2 = []
    for l_data in data:
        save_tmp = []
        for value in l_data:
            tmp = value[0:2]
            if tmp == "异地":
                tmp = "不固定"
            save_tmp.append(tmp)
        new_data1.append(save_tmp)
    for index, value in enumerate(new_data1):
        counter = Counter(value)
        print(top_10[index])
        new_data2.append((top_10[index], counter.most_common(10)))
    return new_data2


def main():
    job_list = get_all_data("select job_position from tb_data")
    top_10 = top_10_job(job_list)
    kvs = get_keys(top_10)
    new_kws = get_new_kws(kvs)
    data = get_address(new_kws)
    data = get_useful_data(new_kws, data)
    print(data)
    c = draw_top10jobs_address.radar_base(data)
    c.render("top_10_jobs_address.html")


if __name__ == '__main__':
    main()
