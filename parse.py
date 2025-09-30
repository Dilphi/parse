# parse.py
import requests
import bs4
import pandas as pd
from urllib.parse import urljoin
from datetime import datetime
import db

BASE_URL = "https://metu.edu.kz/"

def fetch_article_text(url: str) -> str:
    unwanted_phrases = [
        "пр. Аль-Фараби", "050060, Алматы", "Республика Казахстан",
        "Горячая линия для абитуриентов", "Приемная ректора",
        "Офис-регистратор", "Бухгалтерия", "Адрес",
        "Оплатить обучение", "Справедливость в твоих руках"
    ]
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return ""
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        paragraphs = soup.find_all("p")
        if paragraphs:
            return "\n".join(
                p.get_text(strip=True)
                for p in paragraphs
                if p.get_text(strip=True)
                and not any(phrase in p.get_text(strip=True) for phrase in unwanted_phrases)
            )
        spans = soup.find_all("span")
        if spans:
            return "\n".join(
                s.get_text(strip=True)
                for s in spans
                if s.get_text(strip=True)
                and not any(phrase in s.get_text(strip=True) for phrase in unwanted_phrases)
            )
        return ""
    except Exception:
        return ""

def main():
    db.init_db()

    url = urljoin(BASE_URL, "?page=news#gsc.tab=0")
    try:
        response = requests.get(url, timeout=10)
    except Exception as e:
        print("Ошибка запроса главной страницы:", e)
        return

    if response.status_code != 200:
        print(f'Ошибка загрузки страницы : {response.status_code}')
        return

    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    news_titles = soup.find_all(class_="news_block_identical_title")
    news_infos = soup.find_all(class_="news_block_identical_info")

    news_list = []
    # Очищаем индекс перед новой загрузкой (чтобы не дублировалось)
    db.clear_index()

    for title_div, info_div in zip(news_titles[:20], news_infos[:20]):  # ограничение
        title_text = title_div.get_text(strip=True)
        parent_a = title_div.find_parent("a")
        link = urljoin(BASE_URL, parent_a["href"]) if parent_a and parent_a.get("href") else ""
        date_text = " ".join(info_div.get_text(" ", strip=True).split(" ")[0:3])
        news_list.append([title_text, date_text, link])

    # Сохраняем CSV
    df = pd.DataFrame(news_list, columns=["Заголовок", "Дата", "Ссылка"])
    df.to_csv("news.csv", index=False, encoding='utf-8')
    print("✅ Новости сохранены в news.csv")

    # Сохраняем в БД: индекс и содержимое статей (каждая своя таблица)
    for title, date_text, link in news_list:
        nid = db.add_news_index(title, date_text, link)
        db.create_news_table(nid)
        content = ""
        if link:
            content = fetch_article_text(link)
        # сохраняем хоть пустой текст, чтобы было видно что статья обрабатывалась
        db.save_article_text(nid, content, datetime.now().isoformat(timespec='seconds'))
    print("✅ Новости сохранены в SQLite (news.db)")
