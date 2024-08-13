"""
Выберите веб-сайт с табличными данными, который вас интересует.
Напишите код Python, использующий библиотеку requests для отправки HTTP GET-запроса на сайт и получения HTML-содержимого страницы.
Выполните парсинг содержимого HTML с помощью библиотеки lxml, чтобы извлечь данные из таблицы.
Сохраните извлеченные данные в CSV-файл с помощью модуля csv.

Ваш код должен включать следующее:

Строку агента пользователя в заголовке HTTP-запроса, чтобы имитировать веб-браузер и избежать блокировки сервером.
Выражения XPath для выбора элементов данных таблицы и извлечения их содержимого.
Обработка ошибок для случаев, когда данные не имеют ожидаемого формата.
Комментарии для объяснения цели и логики кода.

Примечание: Пожалуйста, не забывайте соблюдать этические и юридические нормы при веб-скреппинге.
"""


import requests
from lxml import html
import csv

url = "https://finance.yahoo.com/trending-tickers/"
response = requests.get(url,headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"},)

tree = html.fromstring(response.content)
# print(tree)

rows = tree.xpath('//table[contains(@class, "W(100%)")]/tbody/tr')
data = []
for row in rows:
    columns = row.xpath(".//td/text()")
    data.append({
        'Symbol': row.xpath(".//td[1]/a/text()")[0].strip(),
        'Name': columns[0].strip(),
        'Last Prise' : row.xpath(".//td[3]/fin-streamer/text()")[0],
        'Market Time' : row.xpath(".//td[4]/fin-streamer/text()")[0],
        'Change' : row.xpath(".//td[5]//span/text()")[0],
        '% Change': row.xpath(".//td[6]//span/text()")[0],
        'Volume' : str(row.xpath(".//td[7]/fin-streamer/text()"))[2:][:-2],
        'Market Cap': str(row.xpath(".//td[8]/fin-streamer/text()"))[2:][:-2]
    })


def save_data(data, file_path):
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            csvwriter = csv.writer(file)
            # Создание заголовков для CSV файла
            csvwriter.writerow(["Symbol", "Name", "Last Price", "Market Time", "Change", "% Change", "Volume", "Market Cap"])
            
            # Запись данных
            for row in data:
                csvwriter.writerow([row["Symbol"], row["Name"], row["Last Prise"], 
                                    row["Market Time"], row["Change"], row["% Change"], 
                                    row["Volume"], row["Market Cap"]])
        print(f"Данные сохранены в {file_path}")
    except IOError as e:
        print(f'Ошибка сохранения данных в {file_path}: {e}')

# Путь для сохранения файла
save_data(data, "Homewook/DZ_4/DZ.csv")