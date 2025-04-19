# import requests
# import sys

# # URL API для получения случайных данных о канабисе
# url = 'https://random-data-api.com/api/cannabis/random_cannabis?size=10'

# # Отправляем GET-запрос к API
# response = requests.get(url)

# # Устанавливаем кодировку ответа в UTF-8
# response.encoding = 'utf-8'

# # Парсим JSON-ответ
# data = response.json()

# # Инициализируем переменную для вывода результатов
# output = []

# # Проходим по каждому элементу в списке данных
# for item in data:
#     # Создаем строку с информацией о текущем элементе
#     strain_info = f"{item['id']}\t{item['uid']}\t{item['strain']}\t{item['cannabinoid_abbreviation']}\t{item['cannabinoid']}\t{item['terpene']}\t{item['medical_use']}\t{item['health_benefit']}\t{item['category']}\t{item['type']}\t{item['buzzword']}\t{item['brand']}"
    
#     # Добавляем эту строку в список вывода
#     output.append(strain_info)

# # Сортируем список вывода по ключу 'strain'
# output.sort(key=lambda x: x.split('\t')[1])  # Используем второй столбец (strain) для сортировки

# # Формируем окончательный вывод
# final_output = '\n'.join(output)

# # Изменяем кодировку на UTF-8
# sys.stdout.reconfigure(encoding='utf-8')

# # Выводим результат
# print(final_output)




import requests
import sys

url = 'https://random-data-api.com/api/cannabis/random_cannabis?size=10' 
response = requests.get(url)
response.encoding = 'utf-8'
r = response.json()

sys.stdout.reconfigure(encoding='utf-8')

for i in r:
    str = f"{i['id']}\t{i['uid']}\t{i['strain']}\t{i['cannabinoid_abbreviation']}\t{i['cannabinoid']}\t{i['terpene']}\t{i['medical_use']}\t{i['health_benefit']}\t{i['category']}\t{i['type']}\t{i['buzzword']}\t{i['brand']}"
    print(str)

print("\nОбработка завершена.")

import requests
import sys



url = 'https://random-data-api.com/api/cannabis/random_cannabis?size=10' # + date.starftime("%Y%m%d")
response = requests.get(url)
response.encoding = 'utf-8'
r = response.json()
sys.stdout.reconfigure(encoding='utf-8')

out = ''
str = ''
for i in r:
    str = f"{i['id']}\t{i['uid']}\t{i['strain']}\t{i['cannabinoid_abbreviation']}\t{i['cannabinoid']}\t{i['terpene']}\t{i['medical_use']}\t{i['health_benefit']}\t{i['category']}\t{i['type']}\t{i['buzzword']}\t{i['brand']}"
    out += str

print(out)

print("--------------------------------------------")
print(str)    



out = ''
str = ''
for i in r:
    str = f"{i['name']}\t{['price']}\n"
    out += str