import requests
import bs4
import pandas as pd

def main():
    url = 'https://metu.edu.kz/?page=news#gsc.tab=0'
    response = requests.get(url)

    # Проверка успешности запроса
    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        # Находим блоки новостей
        news_titles = soup.find_all(class_="news_block_identical_title")
        new_identical_info = soup.find_all(class_="news_block_identical_info")

        print("Актуальные новости:")

        # Список для сохранения
        new_list = []

        for i, (title, info) in enumerate(zip(news_titles[:10], new_identical_info[:10]), start=1):  # первые 10 новостей
            text = info.text.strip()
            clean_info = " ".join(text.split()[:-1])  # убираем лишний элемент (например "Подробнее")
            print(f'{i}. {title.text.strip()} — {clean_info}')

            # Добавляем в список
            new_list.append([title.text.strip(), clean_info])

        # Сохраняем в CSV
        df = pd.DataFrame(new_list, columns=["Заголовок", "Дата"])
        df.to_csv("news.csv", index=False, encoding='utf-8')
        print("✅ Новости сохранены в news.csv")

    else:
        print(f'Ошибка загрузки страницы : {response.status_code}')
