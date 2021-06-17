#!/usr/bin/python
# -*- coding: utf-8-sig -*-
import time
from selenium import webdriver
from typing import List
from urllib.request import urlretrieve


def crawling_kurly(keyword: str) -> List:
    """
    마켓컬리 크롤링 함수
    Args:
        keyword (str): 검색어

    Returns:
        (List[str, str, str, str]): name, price, img_url, description

    """
    options = webdriver.ChromeOptions()
    options.add_argument("headless")  # 웹브라우저를 띄우지 않음
    options.add_argument('disable-gpu')  # gpu 사용안함
    options.add_argument('lang=ko_KR')
    driver = webdriver.Chrome(options=options)

    url = "https://www.kurly.com/"

    driver.get(url)  # 접속시도
    time.sleep(0.5)

    element = driver.find_element_by_name('sword')
    element.send_keys(keyword)
    element.submit()
    time.sleep(1)
    item_list = []

    item_data = driver.find_elements_by_class_name('info')
    time.sleep(2)
    for i in item_data:
        item_list.append(i.text.split("\n"))

    img_datas = driver.find_elements_by_css_selector('img')
    idx = 1
    for i in img_datas:
        img_url = i.get_attribute("src")
        if "https://img-cf.kurly.com/shop/data/goods/" in img_url:
            item_list[idx-1].insert(2, img_url)
            # urlretrieve(img_url, "./img/{}.jpg".format(str(idx).rjust(4, '0')))   # 이미지 다운로드
            idx += 1
    driver.quit()
    return item_list


def crawling_coupang(keyword: str) -> List:
    """
    쿠팡 크롤링 함수
    Args:
        keyword (str): 검색어

    Returns:
        (List[str, str, str]): name, price, img_url

    """
    options = webdriver.ChromeOptions()
    options.add_argument("headless")  # 웹브라우저를 띄우지 않음
    options.add_argument('disable-gpu')  # gpu 사용안함
    options.add_argument('lang=ko_KR')
    driver = webdriver.Chrome(options=options)
    if " " in keyword:
        keyword = keyword.replace(" ", "+")
    url = "https://www.coupang.com/np/search?component=&q={}&channel=user".format(keyword)
    driver.get(url)  # 접속시도
    time.sleep(0.5)
    item_name = driver.find_elements_by_class_name("name")
    item_price = driver.find_elements_by_class_name("price-value")
    item_img = driver.find_elements_by_class_name("search-product-wrap-img")
    result = []
    for name, price, img in zip(item_name, item_price, item_img):
        result.append([name.text, price.text, img.get_attribute("src")])
    driver.quit()

    return result


def crawling_SSG(keyword: str) -> List:
    """
    SSG 크롤링 함수
    Args:
        keyword (str): 검색어

    Returns:
        (List[str, str, str]): name, price, img_url

    """
    options = webdriver.ChromeOptions()
    options.add_argument("headless")  # 웹브라우저를 띄우지 않음
    options.add_argument('disable-gpu')  # gpu 사용안함
    options.add_argument('lang=ko_KR')
    driver = webdriver.Chrome(options=options)
    if " " in keyword:
        keyword = keyword.replace(" ", "+")
    url = "http://emart.ssg.com/search.ssg?target=all&query={}".format(keyword)

    driver.get(url)  # 접속시도
    time.sleep(0.5)

    item_name = driver.find_elements_by_xpath("//div[@class='title']/a[@class='clickable']/em[@class='tx_ko']")
    item_name = [i for i in item_name if i.text.strip() != ""]
    item_price = driver.find_elements_by_class_name("ssg_price")
    item_img = driver.find_elements_by_class_name("i1")
    result = []
    for name, price, img in zip(item_name, item_price, item_img):
        result.append([name.text, price.text, img.get_attribute("src")])
    driver.quit()
    return result


if __name__ == "__main__":
    print(crawling_SSG("떡볶이 떡"))