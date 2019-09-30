import requests
import threading
from concurrent.futures.thread import ThreadPoolExecutor
import pymysql
from selenium import webdriver
from urllib.parse import quote


def main():
    resp = requests.post(url="https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false",
                         data={
                             "Accept": "application/json, text/javascript, */*; q=0.01",
                             "Accept-Encoding": "gzip, deflate, br",
                             "Accept-Language": "zh-CN,zh;q=0.9",
                             "Connection": "keep-alive",
                             "Content-Length": 24,
                             "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                             "Cookie": "user_trace_token=20190621170255-d5ab6466-c9c7-4e1f-b9fa-9ce1cf5603b3; _ga=GA1.2.1474711451.1561107776; LGUID=20190621170256-5c12c311-9403-11e9-a441-5254005c3644; _gid=GA1.2.1620476166.1562584481; index_location_city=%E5%8C%97%E4%BA%AC; LG_HAS_LOGIN=1; hasDeliver=0; privacyPolicyPopup=false; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216bd15244a732e-04194d5a9d6d9f-e343166-1327104-16bd15244a8327%22%2C%22%24device_id%22%3A%2216bd15244a732e-04194d5a9d6d9f-e343166-1327104-16bd15244a8327%22%2C%22props%22%3A%7B%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2275.0.3770.100%22%2C%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; JSESSIONID=ABAAABAAAGGABCB4826D803BF25D6F059552E0F7F2EBD90; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1562584481,1562594043,1562634586,1562651714; LGSID=20190709135514-1f47ea25-a20e-11e9-bdcb-525400f775ce; LG_LOGIN_USER_ID=2c043e3827923986fac2f1981d99269d57bddc2035c1b6a3df6d913c4a94083d; _putrc=4E8210DF149F6DF4123F89F2B170EADC; login=true; unick=%E5%B0%8F%E5%8C%85; gate_login_token=fcc2c8f8e7a86e5de6b2e050c77c35319840515a6065954f8c82a5899ae062da; SEARCH_ID=265dddd9de534fd89c29378f3c08abc7; X_HTTP_TOKEN=e774173ca4a1767992035626518d247977dc2e069a; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1562653029; LGRID=20190709141709-2ed9d646-a211-11e9-a4dc-5254005c3644; TG-TRACK-CODE=search_code",
                             "Host": "www.lagou.com",
                             "Origin": "https://www.lagou.com",
                             "Referer": "https://www.lagou.com/jobs/list_Java?px=default&city=%E5%85%A8%E5%9B%BD",
                             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
                             "X-Anit-Forge-Code": 0,
                             "X-Anit-Forge-Token": None
                         }
                    )
    print(resp.text)


if __name__ == '__main__':
    main()