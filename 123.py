import time
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

# Чтение ФИО из файла
from selenium.webdriver.common.by import By

with open('names.csv', 'r', encoding='utf8') as file:
    employees = file.read().splitlines()



# Создание пустого списка для результатов
results = []

# Запуск браузера
driver = webdriver.Chrome()

# Перебор ФИО сотрудников
for employee in employees:
    # Переход на страницу с проверкой сертификата
    driver.get('https://www.megaputer.ru/produkti/sertifikat/')
    name_input = driver.find_element(by=By.TAG_NAME, value='input')
    button = driver.find_element(by=By.ID, value='certificates-button')
    name_input.send_keys(employee)
    button.click()

    # Ожидание загрузки результатов
    time.sleep(2)

    # Получение HTML-кода страницы
    html = driver.page_source

    # Создание объекта BeautifulSoup
    soup = BeautifulSoup(html, 'lxml')

    # df = pd.DataFrame({'ФИО': [], 'Название': [], 'Дата': []})

    # Поиск элементов с информацией о сертификатах
    data = soup.find('div', id='text1')
    if data.text == 'По данному запросу ничего не найдено':
        results.append([employee, '', ''])
        print(data)
    else:
        name = data.find_all_next('td')
        for n in name:
            t = n.get_text()
            results.append([t])



with open('results.csv', 'w', newline='', encoding='utf8') as file:
    writer = csv.writer(file)
    writer.writerows(results)