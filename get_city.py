import requests
from selenium import webdriver


def main():
    get_cities()


def get_cities():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    # 启动无头浏览器
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.lagou.com/zhaopin/Java/")
    city_list = []
    cities = driver.find_elements_by_css_selector(
        "#filterCollapse > div:nth-child(1) > div.more.more-positions.workPosition > li > a")
    count = len(cities)
    for index, city in enumerate(cities):
        if index != count - 1:
            city_list.append(city.get_attribute("innerText"))
    print(city_list)
    driver.quit()
    return city_list


if __name__ == '__main__':
    main()