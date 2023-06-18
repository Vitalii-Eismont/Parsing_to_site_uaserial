import json
import os.path
import random
import time

import requests
from bs4 import BeautifulSoup as BS

url = "https://uaserial.com/movie"

project_data_list = []
iteration_count = 159
print(f"Всього залишилось: #{iteration_count}")

for item in range(1, 160):
    req = requests.get(url + f"/{item}")
    src = req.text

    folder_name = f"data/data+{item}"

    if os.path.exists(folder_name):
        print("Папка вже існує!")

    else:
        os.mkdir(folder_name)

    with open(f"{folder_name}/index_{item}.html", "w", encoding="utf-8") as file:
        file.write(src)

    with open(f"{folder_name}/index_{item}.html", encoding="utf-8") as file:
        src = file.read()

    soup = BS(src, "lxml")
    articles = soup.find_all("div", class_="item")

    projects_urls = []
    for article in articles:
        project_url = "https://uaserial.com" + article.find("a").get("href")
        projects_urls.append(project_url)


    for project_url in projects_urls:
        req = requests.get(project_url)
        project_name = project_url.split("/")[-1]

        with open(f"{folder_name}/{project_name}.html", "w", encoding="utf-8") as file:
            file.write(req.text)

        with open(f"{folder_name}/{project_name}.html", encoding="utf-8") as file:
            src = file.read()

        soup = BS(src, "lxml")
        project_data = soup.find("div", class_="serial__data flex between")

        try:
            project_names = project_data.find("div", class_="header--title flex column a__start").find("h1", class_="title").text
        except Exception:
            project_names = "No project names"

        try:
            project_original_names = project_data.find("div", class_="header--title flex column a__start").find("div", class_="original").text
        except Exception:
            project_original_names = "No project origenal names"


        try:
            project_photo = "https://uaserial.com" + project_data.find("div", class_="poster").find("img").get("src")
        except Exception:
            project_photo = "No project photo"

        try:
            project_country = project_data.find("div", class_="movie-data-item country flex start").find("div", class_="value").text
        except Exception:
            project_country = "No project country"

        try:
            project_studio = project_data.find("div", class_="movie-data-item studio flex start").find("div", class_="value").text
        except Exception:
            project_studio = "No project studio"

        try:
            project_rating = project_data.find("div", class_="number").text.strip()
        except Exception:
            project_rating = "No project rating"

        try:
            project_ganer = project_data.find("div", class_="movie-data-item genre flex start a__start").text.strip()
        except Exception:
            project_ganer = "No project ganer"

        try:
            project_duration = project_data.find("div", class_="movie-data-item duration flex start").find("div", class_="value").text
        except Exception:
            project_duration = "No project duration"

        try:
            project_release = project_data.find("div", class_="movie-data-item release flex start").find("div", class_="value").text
        except Exception:
            project_release = "No project release"

        try:
            project_text = project_data.find("div", class_="text").text.strip()
        except Exception:
            project_text = "No project text"

        project_data_list.append(
            {
                "Name: ": project_names.strip(),
                "Original names: ": project_original_names,
                "Photo: ": project_photo,
                "Країна: ": project_country,
                "Студія: ": project_studio,
                "Rating: ": project_rating.strip(),
                "Ganer: ": project_ganer.strip(),
                "Time: ": project_duration,
                "Дата релізу: ": project_release.strip(),
                "Опис": project_text,
            }
        )
    iteration_count -= 1
    print(f"Подія #{item} закінчена, залишилось #{iteration_count}")
    if iteration_count == 0:
        print("Збір даних закінчено")

    time.sleep(random.randrange(2, 4))

with open("data/project_data.json", "a", encoding="utf-8") as file:
    json.dump(project_data_list, file, indent=4, ensure_ascii=False)