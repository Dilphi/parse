# main.py
import flet
import cli
import app

def main(page: flet.Page):
    page.title = "Новости МИТУ"
    page.vertical_alignment = flet.MainAxisAlignment.START

    def open_gui(_):
        page.clean()
        app.main(page)  # просто загружаем GUI из app.py
        
    gui_button = flet.ElevatedButton(text="Запустить GUI", on_click=open_gui)
    cli_button = flet.ElevatedButton(text="Загрузить новости в консоли", on_click=lambda _: cli.main())

    page.add(gui_button, cli_button)

if __name__ == "__main__":
    flet.app(target=main)
