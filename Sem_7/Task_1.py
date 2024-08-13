'''Задание 1
- Импортируйте необходимые библиотеки:
selenium, webdriver, By, WebDriverWait, expected_conditions, time
и json.
- Определите User Agent
- Запустите веб-драйвер Chrome.
- Перейдите на страницу канала YouTube.
- Дождитесь загрузки страницы.
- Установите время паузы прокрутки и получите текущую
высоту страницы.'''


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# класс для указания типа селектора
from selenium.webdriver.common.by import By
# класс для ожидания наступления события
from selenium.webdriver.support.ui import WebDriverWait
# включает проверки, такие как видимость элемента на странице, доступность элемента для отклика и т.п.
from selenium.webdriver.support import expected_conditions as EC
# ошибки в selenium
from selenium.webdriver.chrome.options import Options
# работа со всеми возможными функциями
import time

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
#Задается строка User-Agent, позволяющая браузеру "притворяться" другим устройством или браузером для предотвращения блокировок.

chrome_option = Options()
chrome_option.add_argument(f'user-agent={user_agent}')
# chrome_option.add_argument('--ignore-certificate-errors-spki-list')
chrome_option.add_argument('start-maximized')  # хром на весь экран 
# Создается объект Options, в который добавляются настройки. Браузер будет автоматически открываться во весь экран 

driver = webdriver.Chrome(options=chrome_option)
url = 'https://www.youtube.com/@progliveru/videos'
driver.get(url)
#Экземпляр веб-драйвера Chrome создается с заданными параметрами. Затем происходит переход на страницу канала YouTube


# ожидаем подгрузку всех элементов тела
# Используется метод WebDriverWait для ожидания полной загрузки элемента <body> на странице
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

scroll_pause = 2
last_height = driver.execute_script('return document.documentElement.scrollHeight')  # высота экрана
#  Устанавливается время паузы (2 секунды) между итерациями прокрутки. Также определяется начальная высота страницы (last_height)


while True:
    driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);') #window.scrollTo(0, document.documentElement.scrollHeight) позволяет прокрутить страницу в самый низ
    time.sleep(scroll_pause) # time.sleep(scroll_pause) делает паузу между прокрутками, чтобы дать странице время на загрузку новых элементов.
    page_height = driver.execute_script('return document.documentElement.scrollHeight') #page_height обновляется после каждой прокрутки. Если высота страницы не изменилась, цикл прекращается, и программа переходит к следующему блоку кода
    if last_height == page_height:
        break
    last_height = page_height
    print(f'Высота экрана: {last_height}')

print(f'Высота экрана: {page_height}')

driver.quit() # Закрывает браузер и завершает работу веб-драйвера