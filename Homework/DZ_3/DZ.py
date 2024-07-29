from pymongo import MongoClient
import json

client = MongoClient("mongodb://127.0.0.1:27017")
db = client["Houston"]
collection = db["housing"]

# Чтение файла
with open("Sem_3/DZ/houston_housing.json", "r") as file:
    data = json.load(file)

# Вставляем данные в колекцию
collection.insert_many(data)

print("Загрузка прошла успешно")
