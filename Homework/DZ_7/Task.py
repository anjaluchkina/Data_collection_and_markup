from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json

user_agent = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36')

chrome_option = Options()
chrome_option.add_argument(f'user-agent={user_agent}')
chrome_option.add_argument('start-maximized')  # браузер на весь экран

driver = webdriver.Chrome(options=chrome_option)
url = 'https://rushandball.ru/publications'
# Данные с сайта Федерации гандбола России, из вкладки "Новости

try:
    driver.get(url)
    # Ожидаем подгрузку всех элементов страницы.
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    
    scroll_pause = 2
    # Устанавливаю временную паузу между скроллами.
    page_height = driver.execute_script('return document.documentElement.scrollHeight') # Получаю высоту страницы для скроллинга.
    while True:
        driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')  # Скроллю страницу вниз до конца.
        time.sleep(scroll_pause) 
        new_height = driver.execute_script('return document.documentElement.scrollHeight') # Получаю новую высоту страницы после скролла.
        if new_height == page_height: # Если высота не изменилась, значит контент больше нет.
            break
        page_height = new_height

    page_source = driver.page_source  # Извлекаю весь исходный HTML-код загруженной страницы.
    soup = BeautifulSoup(page_source, 'html.parser') # Создаю объект BeautifulSoup для анализа и парсинга HTML

    article_title_xpath = "//*[@id='pubs-wrapper']/div/article/div[1]//div/a"
    metadata_xpath = "//*[@id='pubs-wrapper']/div/article/div[2]/div[2]"
    published_xpath = "//*[@id='pubs-wrapper']/div/article/div[2]/div[1]"
     # Устанавливаю XPath-выражения для извлечения заголовков статей, метаданных (количество просмотров) и даты публикации.

    article_titles = driver.find_elements(By.XPATH, article_title_xpath)
    metadata_elements = driver.find_elements(By.XPATH, metadata_xpath)
    published_elements = driver.find_elements(By.XPATH, published_xpath)
    # Извлекаю элементы на странице по заданным XPath-выражениям.
    
    articles = [] # Создаю список для хранения информации о статьях.
    for i in range(min(len(article_titles), len(metadata_elements), len(published_elements))): # Перебираю индексы элементов и извлекаю данные.
        title = article_titles[i].text
        view = metadata_elements[i].text
        time_ago = published_elements[i].text
        articles.append({'title': title, 'views': view, 'published_date': time_ago}) # Добавляю информацию в список в виде словаря.

   
    #print(articles)

    with open('Homework/DZ_7/article_data.json', 'w', encoding='UTF-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

    print('Данные сохранены в файл Homework/DZ_7/article_data.json')

except Exception as e:
    print(f'Произошла ошибка: {e}')
finally:
    driver.quit()