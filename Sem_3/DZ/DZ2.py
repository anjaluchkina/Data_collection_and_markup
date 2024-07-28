from pymongo import MongoClient
import json

client = MongoClient()
db = client["Houston"]
collection = db["housing"]

try:
    # Вывод первой записи в коллекции
    first_doc = collection.find_one({}, {"_id": False})  # Исключаем _id
    if first_doc:
        pretty_json = json.dumps(first_doc, indent=4, default=str)
        print(pretty_json)

    count = collection.count_documents({})
    print(f"Число записей в БД = {count}")

    # Все цены с адресами
    print("\nЦены на все объекты в коллекции:")
    for doc in collection.find({}, {"address": 1, "price": 1, "_id": False}):
        print(
            f"Адрес: {doc.get('address', 'Не указано')} - Цена: {doc.get('price', 'Не указана')} $"
        )

    # Максимальная и минимальная стоимость домов
    max_price_doc = collection.find_one({}, {"price": 1, "_id": False}, sort=[("price", -1)])
    max_price = max_price_doc["price"] if max_price_doc else None
    print(f"Максимальная цена дома = {max_price}")

    min_price_doc = collection.find_one({}, {"price": 1, "_id": False}, sort=[("price", 1)])
    min_price = min_price_doc["price"] if min_price_doc else None
    print(f"Минимальная цена дома = {min_price}")

    # Средняя стоимость домов
    average_price = collection.aggregate([{"$group": {"_id": None, "avgPrice": {"$avg": "$price"}}}],allowDiskUse=True )
    average_price_list = list(average_price)
    if average_price_list:
        average_price_value = average_price_list[0]["avgPrice"]
        print(f"Средняя цена дома = {average_price_value}")
    else:
        print("Нет доступных данных для расчета средней цены.")

    # Максимальная и минимальная площадь помещений
    max_area_doc = collection.find_one({}, {"area": 1, "_id": False}, sort=[("area", -1)])
    max_area = max_area_doc["area"] if max_area_doc else None
    print(f"Максимальная площадь помещения = {max_area}")

    min_area_doc = collection.find_one({}, {"area": 1, "_id": False}, sort=[("area", 1)])
    min_area = min_area_doc["area"] if min_area_doc else None
    print(f"Минимальная площадь помещения = {min_area}")

    # Все записи с количеством спален
    print("\nЗаписи с количеством спален:")
    for doc in collection.find({}, {"address": 1, "beds": 1, "_id": False}):
        print(f"Адрес: {doc.get('address', 'Не указано')} - Количество спален: {doc.get('beds', 'Не указано')}")

    # Максимальное и минимальное количество спален
    max_beds_doc = collection.find_one({}, {"beds": 1, "_id": False}, sort=[("beds", -1)])
    max_beds = max_beds_doc["beds"] if max_beds_doc else None
    print(f"Максимальное количество спален = {max_beds}")

    min_beds_doc = collection.find_one({}, {"beds": 1, "_id": False}, sort=[("beds", 1)])
    min_beds = min_beds_doc["beds"] if min_beds_doc else None
    print(f"Минимальное количество спален = {min_beds}")

except Exception as e:
    print(f"Произошла ошибка: {e}")