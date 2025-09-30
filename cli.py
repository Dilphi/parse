import db
import parse
import sys

def show_main_menu():
    print("\n=== Новости МИТУ — CLI ===")
    print("1. Обновить/Парсить новости (из сети)")
    print("2. Показать список новостей")
    print("q. Выход")
    print("==========================")

def show_news_list():
    rows = db.list_news()
    if not rows:
        print("Список новостей пуст. Сначала запустите парсер (1).")
        return
    print("\nСписок новостей:")
    for r in rows:
        print(f"{r[0]}. {r[1]} — {r[2]}")
    print("\nВведите номер новости чтобы просмотреть (или 'b' — назад, 'q' — выход).")

def view_article(news_id: int):
    meta = db.get_news_meta(news_id)
    if not meta:
        print("Новость не найдена.")
        return
    print(f"\n📌 {meta[1]} — {meta[2]}")
    content = db.get_latest_article_text(news_id)
    if not content:
        print("Текст статьи пуст или не был скачан.")
    else:
        # показываем первые N символов с опцией показать больше
        pos = 0
        page_len = 1500
        while True:
            chunk = content[pos:pos+page_len]
            print("\n" + chunk)
            pos += page_len
            if pos >= len(content):
                print("\n--- Конец статьи ---")
                break
            cmd = input("\nНажмите Enter чтобы продолжить, 'b' — назад, 's' — сохранить в файл, 'q' — выход: ").strip().lower()
            if cmd == "b":
                return
            if cmd == "s":
                with open("article.txt", "w", encoding="utf-8") as f:
                    f.write(f"{meta[1]}\n{meta[2]}\n\n{content}")
                print("Сохранено в article.txt")
            if cmd == "q":
                sys.exit(0)
        # в конце даём опции
        cmd = input("\n'b' — назад, 's' — сохранить в файл, 'q' — выход: ").strip().lower()
        if cmd == "s":
            with open("article.txt", "w", encoding="utf-8") as f:
                f.write(f"{meta[1]}\n{meta[2]}\n\n{content}")
            print("Сохранено в article.txt")
        if cmd == "q":
            sys.exit(0)

def main():
    db.init_db()
    while True:
        show_main_menu()
        choice = input("Выберите опцию: ").strip().lower()
        if choice == "1":
            print("Запуск парсера... (может занять секунды)")
            parse.main()
            input("Нажмите Enter чтобы продолжить...")
        elif choice == "2":
            while True:
                show_news_list()
                cmd = input("Ваш ввод: ").strip().lower()
                if cmd == "b":
                    break
                if cmd == "q":
                    print("Выход.")
                    sys.exit(0)
                try:
                    nid = int(cmd)
                    view_article(nid)
                except ValueError:
                    print("Неверный ввод. Введите номер новости, 'b' или 'q'.")
        elif choice == "q":
            print("Выход.")
            break
        else:
            print("Неверный выбор. Попробуйте ещё раз.")

if __name__ == "__main__":
    main()
