import requests
import bs4
import pandas as pd
from urllib.parse import urljoin

def main():
    BASE_URL = "https://metu.edu.kz/"

    url = urljoin(BASE_URL, "?page=news#gsc.tab=0")
    response = requests.get(url)

    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        # Находим блоки новостей
        news_titles = soup.find_all(class_="news_block_identical_title")
        news_infos = soup.find_all(class_="news_block_identical_info")

        print("Актуальные новости:")

        news_list = []

        for i, (title_div, info_div) in enumerate(zip(news_titles[:10], news_infos[:10]), start=1):
            # Заголовок
            title_text = title_div.get_text(strip=True)

            # Ссылка (родительский <a>)
            parent_a = title_div.find_parent("a")
            link = urljoin(BASE_URL, parent_a["href"]) if parent_a and parent_a.get("href") else ""

            # Дата
            date_text = info_div.get_text(" ", strip=True).split(" ")[0:3]  # например "19 Сентябрь 2025"
            date_text = " ".join(date_text)

            print(f"{i}. {title_text} — {date_text}")
            news_list.append([title_text, date_text, link])

        # BUGFIX: сохранение CSV и сообщение должны быть вне цикла, иначе файл перезаписывается на каждом шаге
        df = pd.DataFrame(news_list, columns=["Заголовок", "Дата", "Ссылка"])
        df.to_csv("news.csv", index=False, encoding='utf-8')
        print("✅ Новости сохранены в news.csv")

    else:
        print(f'Ошибка загрузки страницы : {response.status_code}')
