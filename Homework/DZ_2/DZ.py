"""
Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ и извлечь информацию 
о всех книгах на сайте во всех категориях: название, цену, количество товара в наличии (In stock (19 available)) в формате integer, описание.
"""

import requests  # Используется для отправки HTTP-запросов
from bs4 import BeautifulSoup  # Для парсинга HTML и XML документов
from datetime import datetime  # Для работы с датами и временем
import re  # Для работы с регулярными выражениями
import json  # Для работы с форматом данных JSON


# Основаная функция
def get_box_data():

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    release_link = []

    soup = BeautifulSoup(response.text, features="html.parser")  # парсим сайт.
    site_elements = soup.find_all("article", class_="product_pod")
    # print(soup.prettify()) # проверяем нахождения сведений о книге.

    for elements in site_elements:
        href_element = elements.h3.a["href"]  # ссылку на страницу товара.
        href_response = requests.get(
            "http://books.toscrape.com/catalogue/" + href_element
        )  # создаём правильный url книги.

        url_book = BeautifulSoup(
            href_response.text, "html.parser"
        )  # парсим страницу книги.
        book_elements = url_book.find_all(
            "article", class_="product_page"
        )  # заходим в книгу.

        for book in book_elements:
            try:
                title = book.find(
                    "div", class_="col-sm-6 product_main"
                ).h1.text  # получаем название.
                price = float(
                    book.find("p", class_="price_color").text[1:].replace("£", "")
                )  # получаем цену.
                stock_str = book.find(
                    "p", class_="instock availability"
                ).text.strip()  # количество товара в наличии.
                stock = re.search(
                    r"\d+", stock_str
                )  # регулярное выражение для извлечения числа.
                number_str = stock.group()  # извлекаем число как строку.
                number_int = int(number_str)  # преобразуем строку в число.
                stock_int = (
                    re.sub(r"\d+", str(number_int), stock_str) if stock else 0
                )  # подменяем строковое число на интовое число.

                # Добавляем в словарь.
                data_all = {
                    "Title": title,
                    "Price": price,
                    "Stock_int": stock_int,
                }
                release_link.append(data_all)
            except Exception as e:
                print(f"Error parsing book: {e}")
    return release_link


# Сохранение в json
def save_DZ_json(file_name, all_books_data):
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(all_books_data, file, ensure_ascii=False, indent=4)
            print(f"Data saved to {file_name}")
    except Exception as e:
        print(f"Error save data to < {file_name} > : {e}")


# Запуск прогарммы
if __name__ == "__main__":
    url = "http://books.toscrape.com/catalogue/page-1.html"  # URL страницы, которую распарсить
    all_books_data = get_box_data()
save_DZ_json("Homewook/DZ_2/save_DZ_json", all_books_data)