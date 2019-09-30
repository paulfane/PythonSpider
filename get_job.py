import requests
from selenium import webdriver


def main():
    get_jobs()


def get_jobs(driver):
    job = []
    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # # 启动无头浏览器
    # driver = webdriver.Chrome(options=options)
    driver.get("https://www.lagou.com/")
    chengdu = driver.find_element_by_css_selector("#changeCityBox > ul > li:nth-child(7) > a")
    chengdu.click()
    menu = driver.find_element_by_css_selector("#sidebar > div > div:nth-child(1) > div.menu_sub.dn")
    hrefs = menu.find_elements_by_css_selector("dl a")
    print(len(hrefs))
    for href in hrefs:
        job.append(href.get_attribute("href"))
    driver.quit()
    return job


if __name__ == '__main__':
    main()