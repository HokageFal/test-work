import requests
from bs4 import BeautifulSoup
import csv


def get_animals_count():
    url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
    base = "https://ru.wikipedia.org"
    counts = {}
    processed_pages = set()

    while url:
        try:

            if url in processed_pages:
                print("Обнаружен цикл в ссылках, прекращаем обработку")
                break

            processed_pages.add(url)

            print(f"Обрабатываем страницу: {url}")
            page = requests.get(url, timeout=10)
            page.raise_for_status()
            soup = BeautifulSoup(page.text, 'html.parser')

            category_div = soup.find('div', class_='mw-category-columns')
            if not category_div:
                print("Не найден блок с категориями")
                break

            groups = category_div.find_all('div', class_='mw-category-group')

            for group in groups:
                letter = group.find('h3').text.strip()
                items = group.find_all('li')
                counts[letter] = counts.get(letter, 0) + len(items)
                print(f"Буква {letter}: +{len(items)}")

            next_page = soup.find('a', string='Следующая страница')
            if not next_page:
                print("Не найдена ссылка на следующую страницу")
                break

            url = base + next_page['href']
            print(f"Переход на следующую страницу: {url}")

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            break
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            break

    return counts


def save_counts(counts):
    with open('beasts.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for letter in sorted(counts.keys()):
            writer.writerow([letter, counts[letter]])


if __name__ == '__main__':
    print("Начинаем сбор данных...")
    animals = get_animals_count()
    save_counts(animals)
    print(f"Готово! Собрано данных по {len(animals)} буквам. Результат в beasts.csv")