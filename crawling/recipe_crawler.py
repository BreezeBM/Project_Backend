import requests


import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys

import pandas as pd


def search_recipe_list(cook_name: str, base_url: str):
    """
    음식이름으로 recipe url 목록을 찾는 함수
    Args:
        cook_name (str) : 음식이름
        base_url: 만개의 레시피 경로

    Returns:
        list : 레시피 url 목록
    """
    search_url = "{}/recipe/list.html?q={}&order=reco&page=1".format(base_url, cook_name)
    driver = Chrome(executable_path="chromedriver.exe")
    driver.get(url=search_url)
    driver.implicitly_wait(time_to_wait=3)
    driver.maximize_window()
    body = driver.find_element_by_tag_name("body")
    num_of_pagedowns = 2
    while num_of_pagedowns:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
        num_of_pagedowns -= 1
    # 모든 페이지 source 가져오기
    html0 = driver.page_source
    driver.close()
    html = BeautifulSoup(html0, 'html.parser')
    recipe_tag = html.find_all(href=re.compile('^/recipe/[0-9]+'))
    result = [path.attrs["href"] for path in recipe_tag]
    print(result)
    return result


def search_recipe_info(url: str):
    """
    recipe url을 가지고 요리정보를 가지고 오는 함수
    Args:
        url (str): recipe url

    Returns:
        List : [레시피 제목, 메인 이미지, 재료, 조리순서, 조리순서 이미지]

    """
    driver = Chrome(executable_path="chromedriver.exe")
    driver.get(url=url)
    driver.implicitly_wait(time_to_wait=3)
    driver.maximize_window()
    body = driver.find_element_by_tag_name("body")
    num_of_pagedowns = 5
    while num_of_pagedowns:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
        num_of_pagedowns -= 1
    # 모든 페이지 source 가져오기
    html0 = driver.page_source
    driver.close()
    html = BeautifulSoup(html0, 'html.parser')
    main_img = html.find("img", id="main_thumbs").attrs["src"]
    # print("main_img : ", main_img)
    title = html.find("h3").text
    # print("title : ", title)
    description = html.find("div", id="recipeIntro").text.strip()
    # print("description", description)
    ingredients = []
    for tag in html.find_all("a", href=re.compile("^javascript:viewMaterial")):
        ingre = tag.find("li").text.split("\n")[0].strip()
        capa = tag.find("li").text.split("\n")[1]
        ingredients.append((ingre, capa))
    # print("ingredients : ", ingredients)
    recipe = html.find_all("div", id=re.compile("^stepdescr"))  # 조리순서
    recipe_steps = [i.text for i in recipe]
    # print("recipe_steps : ", recipe_steps)
    recipe_img = html.find_all("div", id=re.compile("^stepimg"))
    recipe_imgs = [i.find("img").attrs["src"] for i in recipe_img]
    # print("recipe_imgs : ", recipe_imgs)
    result = [title, main_img, str(ingredients[1:-1]), recipe_steps, recipe_imgs]
    return result


def make_cook_dataset(cook_list: list):
    """

    Args:
        cook_list (list): 요리이름을 인자로 담은 리스트

    Returns:

    """
    base_url = "http://www.10000recipe.com"
    result = []
    for cook_name in cook_list:
        recipe_path_list = search_recipe_list(cook_name, base_url)
        for path in recipe_path_list:
            recipe_url = base_url + path
            recipe_info = search_recipe_info(recipe_url)
            recipe_info = [cook_name, recipe_url] + recipe_info
            result.append(recipe_info)

    df = pd.DataFrame(result, columns=["cook_name", "recipe_url", "title", "main_img_path", "ingredients",
                                       "recipe_steps", "recipe_imgs"])
    df.to_csv("recipe.csv", encoding="CP949", index=False)


if __name__ == '__main__':
    cook_names = ["떡볶이", "김밥", "파스타"]
    make_cook_dataset(cook_names)
    # df = pd.read_csv("./recipe.csv", encoding="CP949")
    # cook_dic = {"떡볶이": [], "김밥": [], "파스타": []}
    # for cook_name in cook_dic.keys():
    #     cook_df = df[df["cook_name"] == cook_name]
    #     ingredients_df = cook_df["ingredients"]
    #     for i in ingredients_df:
    #         a = i[2:-1].replace("'", "")
    #         a = a.replace("(", "").split(")")
    #         for j in a:
    #             cnt = len(j.split(","))
    #
    #             if cnt == 1:
    #                 continue
    #             elif cnt == 2:
    #                 ingre, capa = j.split(",")
    #             elif cnt == 3:
    #                 _, ingre, capa = j.split(",")
    #             else:
    #                 print(j.split(","))
    #                 raise Exception("예외처리해야합니다.")
    #             cook_dic[cook_name].append((ingre.strip(), capa.strip()))
    #
    # print(cook_dic)


