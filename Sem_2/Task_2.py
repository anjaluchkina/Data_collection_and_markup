"""
Напишите сценарий на языке Python, чтобы получить ссылки на релизы фильмов со страницы "International Box Office" на сайте Box Office Mojo.
Сохраните ссылки в списке и выведите список на консоль.

Требования:

- Используйте библиотеку requests для запроса веб-страницы.
- Используйте Beautiful Soup для парсинга HTML-содержимого веб-страницы.
- Найдите все ссылки в колонке #1 Release веб-страницы.
- Используйте библиотеку urllib.parse для объединения ссылок с базовым URL.
- Сохраните ссылки в списке и выведите список на консоль.
"""

from bs4 import BeautifulSoup  # type: ignore
import requests  # type: ignore
import urllib.parse
import pandas as pd  # type: ignore

# Запрос веб-страницы
url = "https://www.boxofficemojo.com/intl/?ref_=bo_nb_hm_tab"
response = requests.get(url)

# Парсинг HTML-содержимого веб-страницы с помощью Beautiful Soup
soup = BeautifulSoup(response.content, "html.parser")
# print(soup.prettify())

# Вывод ссылок на
release_link = []
for link in soup.find_all(
    "td", {"class": "a-text-left mojo-field-type-release mojo-cell-wide"}
):
    a_tag = link.find("a")
    if a_tag:
        release_link.append(a_tag.get("href"))
# Объединение ссылок с базовым URL-адресом для создания списка URL-адресов
url_joined = [
    urllib.parse.urljoin("https://www.boxofficemojo.com", link) for link in release_link
]
# Поиск таблицы с данными и ее заголовков
table = soup.find("table", {"class": "a-bordered"})
headers = [header.text.strip() for header in table.find_all("th") if header.text]
# Извлечение данных из таблицы построково и сохранение их в списке словарей
data = []
for row in table.find_all("tr"):
    row_data = {}
    cell = row.find_all("td")
    if cell:
        row_data[headers[0]] = cell[0].find("a").text if cell[0].find("a") else ""
        row_data[headers[1]] = cell[1].find("a").text if cell[1].find("a") else ""
        row_data[headers[2]] = cell[2].text
        row_data[headers[3]] = cell[3].find("a").text if cell[3].find("a") else ""
        row_data[headers[4]] = (
            cell[4].find("a").text.strip() if cell[4].find("a") else ""
        )
        row_data[headers[5]] = cell[5].text.replace("$", "").replace(",", " ")
        data.append(row_data)

# Конвертация списка словарей в pandas DataFrame и его вывод
df = pd.DataFrame(data)
print(df)