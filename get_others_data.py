import lagou
import pymysql


def get_data(conn, start, step):
    data = []
    try:
        with conn.cursor() as cursor:
            cursor.execute("select job_position, job_company, job_salary, \
                               job_address, job_info from tb_data limit %s, %s", (start, step))
            for res in cursor.fetchall():
                tmp = (res[0], res[1], res[2], res[3], res[4])
                data.append(tmp)
    except pymysql.MySQLError as err:
        print(err)
    return data


def save_data(conn, data):
    try:
        with conn.cursor() as cursor:
            cursor.executemany("insert into tb_data(job_position, job_company, job_salary, job_address, job_info) values(%s, %s, %s, %s, %s)", data)
            print("OK")
    except pymysql.MySQLError as err:
        # 应该pass掉
        pass


def main():
    conn = pymysql.connect(host="127.0.0.1", port=3306, database="spider",
                           user="root", password="123456", charset="utf8", autocommit=True)
    for _ in range(0, 5):
        for page in range(0, 100000, 1000):
            data = get_data(conn, page, 1000)
            save_data(conn, data)


if __name__ == '__main__':
    main()