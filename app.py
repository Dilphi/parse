import flet
from flet import (
    Page, Column, Text, ElevatedButton,
    ListView, ListTile, IconButton, AppBar,
    Row, Icon, Icons
)
import parse
import db
import threading
from datetime import datetime


def run_parse_in_thread(page, load_news_to_ui):
    def target():
        parse.main()
        page.invoke_method(load_news_to_ui)
    th = threading.Thread(target=target, daemon=True)
    th.start()



def main(page: Page):
    page.title = "Новости МИТУ"
    page.vertical_alignment = "start"
    db.init_db()

    header = AppBar(
        title=Text("Новости МИТУ"),
        actions=[
            IconButton(Icons.CLOSE, on_click=lambda e: page.window_close())
        ]
    )
    page.appbar = header

    news_list_view = ListView(expand=1, spacing=8)
    content_column = Column()
    main_column = Column(expand=True)
    page.add(main_column)

    def load_news_to_ui():
        news_list_view.controls.clear()
        rows = db.list_news()

        if not rows:
            news_list_view.controls.append(
                Text("Список пуст. Нажмите 'Обновить' чтобы загрузить новости.")
            )
        else:
            for nid, title, date, link in rows:
                def make_on_click(i):
                    def on_click(e):
                        show_article(i)
                    return on_click

                lt = ListTile(
                    title=Text(title, weight="bold"),
                    subtitle=Text(date),
                    leading=Icon(Icons.FEED),
                    on_click=make_on_click(nid),
                )
                news_list_view.controls.append(lt)

        show_list_view(update=False)

    def show_article(news_id: int):
        meta = db.get_news_meta(news_id)
        if not meta:
            return
        title, date = meta[1], meta[2]
        content_column.controls.clear()
        content_column.controls.append(Text(f"{title} — {date}", weight="bold"))
        text = db.get_latest_article_text(news_id)
        content_column.controls.append(Text(text if text else "Текст статьи недоступен."))
        back_btn = ElevatedButton("Назад", on_click=lambda e: show_list_view())
        content_column.controls.append(back_btn)

        main_column.controls.clear()
        main_column.controls.append(content_column)
        page.update()

    def show_list_view(update=True):
        main_column.controls.clear()
        footer = Row([
            ElevatedButton("Обновить/Парсить", on_click=on_refresh),
            ElevatedButton("Закрыть", on_click=lambda e: page.window_close())
        ])
        main_column.controls.append(news_list_view)
        main_column.controls.append(footer)
        if update:
            page.update()

    def on_refresh(e):
        rows = db.list_news()
        today = datetime.today().strftime("%d.%m.%Y")

        if rows and any(today in r[2] for r in rows):
            # если уже есть новости за сегодня
            news_list_view.controls.clear()
            news_list_view.controls.append(Text("Новости актуальны, парсинг не требуется."))
            page.update()
        else:
            news_list_view.controls.clear()
            news_list_view.controls.append(Text("Идёт парсинг..."))
            page.update()
            run_parse_in_thread(page, load_news_to_ui)

    # Инициализация
    load_news_to_ui()
    page.update()


if __name__ == "__main__":
    flet.app(target=main)
