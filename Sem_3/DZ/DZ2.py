from pymongo import MongoClient
import json

client = MongoClient()
db = client["Houston"]
collection = db["housing"]


# вывод первой записи в коллекции
all_docs = collection.find()
first_doc = all_docs[0]


# вывод объекта json
pretty_json = json.dumps(first_doc, indent=4, default=str)
print(pretty_json)

count = collection.count_documents({})
print(f"Число записей в БД = {count}")


# Все цены с адресами
print("\nЦены на все объекты в коллекции:")
for doc in collection.find():
    print(
        f"Адрес: {doc.get('address', 'Не указано')} - Цена: {doc.get('price', 'Не указана')} $"
    )


# Максимальная и минимальная стоимость домов
max_price = collection.find_one(sort=[("price", -1)])["price"]
print(f"Максимальная цена дома = {max_price}")
min_price = collection.find_one(sort=[("price", 1)])["price"]
print(f"Минимальная цена дома = {min_price}")

# Средняя стоимость домов
average_price = collection.aggregate(
    [{"$group": {"_id": None, "avgPrice": {"$avg": "$price"}}}]
)
average_price_list = list(average_price)
if average_price_list:
    average_price_value = average_price_list[0]["avgPrice"]
    print(f"Средняя цена дома = {average_price_value}")
else:
    print("Нет доступных данных для расчета средней цены.")


# Максимальная и минимальная площадь помещений
max_area = collection.find_one(sort=[("area", -1)])
max_area = max_area["area"] if max_area else None
print(f"Максимальная площадь помещения = {max_area}")

min_area = collection.find_one(sort=[("area", 1)])
if min_area and "area" in min_area:
    print(f"Минимальная площадь помещения = {min_area['area']}")
else:
    print("Не удалось найти минимальную площадь помещения.")


# Все записи с количеством спален
print("\nЗаписи с количеством спален:")
for doc in collection.find():
    print(
        f"Адрес: {doc.get('address', 'Не указано')} - Количество спален: {doc.get('beds', 'Не указано')}"
    )
else:
    print("В коллекции нет записей.")


# Максимальное и минимальное количество спален
max_beds = collection.find_one(sort=[("beds", -1)])["beds"]
print(f"Максимальное количество спален = {max_beds}")

min_beds = collection.find_one(sort=[("beds", 1)])
if min_beds and "beds" in min_beds:
    print(f"Минимальное количество спален = {min_beds['beds']}")
else:
    print("Не удалось найти минимальное количество.")
