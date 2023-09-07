import csv
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

try:
    with open('names.csv', 'r', encoding='utf8') as file:
        employees = file.read().splitlines()

    results = []
    driver = webdriver.Chrome()

    for employee in employees:
        driver.get('https://www.megaputer.ru/produkti/sertifikat/')
        name_input = driver.find_element(by=By.TAG_NAME, value='input')
        button = driver.find_element(by=By.ID, value='certificates-button')
        name_input.send_keys(employee)
        button.click()

        time.sleep(2)

        html = driver.page_source

        soup = BeautifulSoup(html, 'lxml')

        data = soup.find('div', id='text1')

        if data.text == 'По данному запросу ничего не найдено':
            result = {
                'ФИО': employee,
                'Название': '',
                'Дата': ''
            }
            results.append(result)
        else:
            elements = driver.find_elements(By.TAG_NAME, value='td')
            fio_value = employee
            for i in range(1, len(elements), 2):
                result = {
                    'ФИО': fio_value,
                    'Название': elements[i].text,
                    'Дата': elements[i + 1].text
                }
                results.append(result)

    with open('results.csv', 'w', encoding='utf8', newline='') as csvfile:
        fieldnames = ['ФИО', 'Название', 'Дата']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
