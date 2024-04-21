import requests
import json
from bs4 import BeautifulSoup
import re
import geotools
# Making a GET request
r = requests.get('https://astana.citypass.kz/ru/category/muzei-i-galerei/')

# check status code for response received
# success code - 200
print(r)

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')
links = []


# STAGE 1 - get links

cards = soup.find_all('div', class_="col-lg-4")
for card in cards:
    info = card.find('a', class_='sights__item--btn sights__item--btn-linck')
    if info:
        links.append(info["href"])


# STAGE 2 - get datas from links

def dump_data():
    datas = []

    for link in links:
        data = {
            "name": None,
            "description": None,
            "geo": None,
            "schedule": None,
            "buses": None,
            "ticket": None,
            "contact": None

        }

        r = requests.get(f'{link}')
        soup = BeautifulSoup(r.content, 'html.parser')
        data["name"] = soup.find(
            "div", class_="object_content--title").get_text().strip()
        data["description"] = "".join(
            [i.get_text() for i in soup.find_all('div', class_="object_content--desc")])
        # print(data["description"])
        data["geo"] = geotools.get_coords_by_name(
            soup.find('div', class_="object__info--adres").get_text().strip())
        if data["geo"] is None:
            continue
        try:
            data["schedule"] = soup.find("div", class_="object_content--right-list object_content--timetable").find("div",
                                                                                                                    class_="object_content-one").get_text().strip() + " " + soup.find("div", class_="object_content--right-list object_content--timetable").find("div",                                                                                                                                                                                                                                           class_="object_content-too").get_text().strip()
            data["buses"] = [re.sub(r'\D', '',  text.get_text().replace(" ", "")) for text in soup.find(
                "div", class_="object_content--right-list object_content--right-list-blue object_content--get").find_all("span")]
            data["contact"] = soup.find(
                "div", class_="object__info--email object__info--phone-repeater").find('a').get_text().strip()
        except:
            pass
        datas.append(data)
        print(data["name"], data["geo"])
        # print(soup)

    with open("data.json", 'w', encoding="utf-8") as file:
        # 'indent' for pretty-printing
        json.dump(datas, file, indent=4, ensure_ascii=False)
