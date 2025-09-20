import flet
import parse
import os
import pandas as pd

def main(page: flet.Page):
    page.title = "Новости МИТУ"
    page.vertical_alignment = flet.MainAxisAlignment.START

    news_container = flet.Column()
    page.add(news_container)

   
    def show_news(_=None):
        parse.main()
        news_container.controls.clear()
        if os.path.exists("news.csv"):
            df = pd.read_csv("news.csv", encoding='utf-8')
            for _, row in df.iterrows():
                news_container.controls.append(flet.Text(f"{row['Заголовок']} — {row['Дата']}"))
            news_container.controls.append(flet.Text("Новости успешно загружены и сохранены в news.csv"))
        else:
            news_container.controls.append(flet.Text("Файл news.csv не найден. Пожалуйста, сначала загрузите новости."))
        page.update()

    def save_news(_=None):
        if os.path.exists("news.txt"):
            with open("news.txt", "r", encoding="utf-8") as file:
                news = file.readlines()
            news_container.controls.clear()
            for item in news:
                news_container.controls.append(flet.Text(item.strip()))
            page.update()
        else:
            news_container.controls.clear()
            news_container.controls.append(flet.Text("Файл news.txt не найден. Пожалуйста, сначала загрузите новости."))
            page.update()


    def load_news(_=None):
        show_news()
        news_container.controls.clear()
        if os.path.exists("news.cvs"):
            df = pd.read_csv("news.csv", encoding='utf-8')
            for _, row in df.iterrows():
                news_container.controls.append(flet.Text(f"{row['Заголовок']} — {row['Дата']}"))
            news_container.controls.append(flet.Text("Новости успешно загружены и сохранены в news.csv"))
        else:
            news_container.controls.append(flet.Text("Файл news.csv не найден. Пожалуйста, сначала загрузите новости."))
        page.update()

    show_button = flet.ElevatedButton(text="Показать новости", on_click=show_news)
    save_button = flet.ElevatedButton(text="Сохранить новости", on_click=save_news)
    load_button = flet.ElevatedButton(text="Загрузить новости", on_click=load_news)

    page.add(show_button)
    page.add(save_button, load_button)
    

if __name__ == '__main__':
    flet.app(target=main)