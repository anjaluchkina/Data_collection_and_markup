"""
- Импортируйте MongoClient и json.
- Cоздайте экземпляр клиента для подключения к MongoDB.
- Подключитесь к базе данных 'town_cary' и коллекции 'crashes'.
- Найдите первый документ в коллекции и распечатайте его в формате JSON.
- Используйте функцию count_documents(), чтобы получить общее количество документов в коллекции.
- Отфильтруйте документы по критерию "properties.fatalities", равному "Yes", и подсчитайте количество совпадающих документов.
- Используйте проекцию для отображения только полей "properties.lightcond" и "properties.weather" для документов с "properties.fatalities" равным "Yes".
"""

"""
- Используйте операторы $lt и $gte для подсчета количества документов с "properties.month" меньше 6 и больше или равно 6, соответственно.
- Используйте оператор $regex для подсчета количества документов, содержащих слово "rain" в поле "properties.weather", игнорируя регистр.
- Используйте оператор $in для подсчета количества документов, в которых "properties.rdclass" является либо "US ROUTE", либо "STATE SECONDARY ROUTE".
- Используйте оператор $all для подсчета количества документов, в которых "properties.rdconfigur" содержит как "TWO-WAY", так и "DIVIDED".
- Используйте оператор $ne для подсчета количества документов, у которых "properties.rdcondition" не равно "DRY".
"""

from pymongo import MongoClient
import json

client = MongoClient()
db = client["town_cary"]
collection = db["crashes"]


# вывод первой записи в коллекции
all_docs = collection.find()
first_doc = all_docs[0]


# вывод объекта json
pretty_json = json.dumps(first_doc, indent=4, default=str)
print(pretty_json)

# коунтер

count = collection.count_documents({})
print(f"число записей в бзд = {count}")

# по всему документу
query = {"properties.fatalities": "Yes"}
print(f"Кол-во документов с погибшими :{collection.count_documents(query)}")

# Используйте проекцию для отображения только полей "properties.lightcond" и "properties.weather" для документов с "properties.fatalities" равным "Yes".
query = {"properties.fatalities": "Yes"}
proection = {"properties.lightcond": 1, "properties.weather": 1, "_id": 0}
doc_project = collection.find(query, proection)
for doc in doc_project:
    print(doc)

# Используйте операторы $lt и $gte для подсчета количества документов с "properties.month" меньше 6 и больше или равно 6, соответственно.
query = {"properties.month": {"$lt": "6"}}
print(
    f"Кол-во документов за период меньше 6 месяцев: {collection.count_documents(query)}"
)

query = {"properties.month": {"$gte": "6"}}
print(
    f"Кол-во документов за период более 6 месяцев: {collection.count_documents(query)}"
)

# Используйте оператор $regex для подсчета количества документов, содержащих слово "rain" в поле "properties.weather", игнорируя регистр.
query = {"properties.weather": {"$regex": "rain", "$options": "i"}}
print(
    f"Кол-во документов об авариях во время дождя: {collection.count_documents(query)}"
)

# Используйте оператор $in для подсчета количества документов, в которых "properties.rdclass" является либо "US ROUTE", либо "STATE SECONDARY ROUTE".
# Используйте оператор $all для подсчета количества документов, в которых "properties.rdconfigur" содержит как "TWO-WAY", так и "DIVIDED".

query = {"properties.rdclass": {"$in": ["US ROUTE", "STATE SECONDARY ROUTE"]}}
print(
    f"Кол-во документов об авариях на дорогах US ROUTE или STATE SECONDARY ROUTE: {collection.count_documents(query)}"
)

query = {"properties.rdconfigur": {"$all": ["TWO-WAY", "DIVIDED"]}}
print(
    f"Кол-во документов об авариях на дорогах TWO-WAY или DIVIDED: {collection.count_documents(query)}"
)

# Используйте оператор $ne для подсчета количества документов, у которых "properties.rdcondition" не равно "DRY".
query = {"properties.rdcondition": {"$ne": "DRY"}}
print(
    f"Кол-во документов об авариях не на дорогах DRY: {collection.count_documents(query)}"
)
