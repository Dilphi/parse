import requests
import bs4
import pandas as pd
import parse

def main():
    # Сначала парсим и сохраняем новости
    parse.main()

    # Загружаем список новостей из файла CSV
    try:
        df = pd.read_csv("news.csv", encoding="utf-8")
        news_list = df.values.tolist()
    except Exception as e:
        print("Ошибка при загрузке news.csv:", e)
        return

    # CLI-выбор
    stat = input("Введите номер статьи (1-10), или 0 для выхода: ")

    try:
        stat_int = int(stat)
    except ValueError:
        stat_int = None

    if stat_int is not None and 1 <= stat_int <= len(news_list):
        selected = news_list[stat_int - 1]
        print(f"\n📌 Вы выбрали новость:\n{selected[0]} — {selected[1]}")
        print(f"Ссылка: {selected[2] if selected[2] else '❌ Ссылки нет'}")

        if not selected[2]:  # если ссылки нет
            print("⚠ У этой новости нет отдельной страницы.")
            return

        # Загружаем текст статьи
        response = requests.get(selected[2])
        if response.status_code == 200:
            article_soup = bs4.BeautifulSoup(response.text, 'html.parser')
            paragraphs = article_soup.find_all("p")
            article_text = "\n".join(
                p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)
            )

            print("\n=== Текст статьи ===\n")
            print(article_text[:1500], "..." if len(article_text) > 1500 else "")

            # Сохраняем в файл
            with open("article.txt", "w", encoding="utf-8") as f:
                f.write(f"{selected[0]}\n{selected[1]}\n\n{article_text}")
            print("💾 Статья сохранена в article.txt")

        else:
            print(f'Ошибка загрузки статьи: {response.status_code}')

    elif stat_int == 0:
        print("Выход.")
    else:
        print("Некорректный выбор статьи.")


if __name__ == "__main__":
    main()
