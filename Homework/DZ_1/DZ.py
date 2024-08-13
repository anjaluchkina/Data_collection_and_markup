"""
Домашнее задание
1. Ознакомиться с некоторые интересными API.
https://docs.ozon.ru/api/seller/
https://developers.google.com/youtube/v3/getting-started
https://spoonacular.com/food-api

2. Потренируйтесь делать запросы к API.
Выберите публичный API, который вас интересует, и потренируйтесь делать API-запросы с помощью Postman. Поэкспериментируйте с различными типами запросов и попробуйте получить различные типы данных.

3. Сценарий Foursquare
- Напишите сценарий на языке Python, который предложит пользователю ввести интересующую его категорию (например, кофейни, музеи, парки и т.д.).
- Используйте API Foursquare для поиска заведений в указанной категории.
- Получите название заведения, его адрес и рейтинг для каждого из них.
- Скрипт должен вывести название и адрес и рейтинг каждого заведения в консоль.
"""

import requests
import json

# Ваши учетные данные API
client_id = "__"
client_secret = "__"

# Конечная точка API
endpoint = "https://api.foursquare.com/v3/places/search"
headers = {
    "Accept": "application/json",
    "Authorization": "fsq3laGYApdCXFXSC8CqIspWfxriz8IA9H988UGMfT6K4os=",
}

city = input("Введите название города: ")
place = input("Введите тип заведения: ")

params = {
    "client_id": client_id,
    "client_secret": client_secret,
    "near": city,
    "query": place,
}
response = requests.get(endpoint, params=params, headers=headers)

if response.status_code == 200:
    data = json.loads(response.text)
    values = data["results"]
    for value in values:
        print("Название:", value["name"])
        print("Адрес:", value["location"]["formatted_address"])
        print("Рейтинг:", value.get("rating", "Рейтинг не найден"))
        print("\n")
else:
    print(f"Ошибка: {response.status_code}")