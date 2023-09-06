import csv
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

with open('names.csv', 'r', encoding='utf8') as file:
    employees = file.read().splitlines()

driver = webdriver.Chrome()

with open('results.csv', 'a', newline='', encoding='utf8') as file:
    writer = csv.writer(file)

    results = []
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
            results.append(employee)
            results.append('')
            results.append('')
            writer.writerow(results)
            results = []
            print(data)
        else:
            name = data.find_all_next('td')
            for n in name:
                t = n.get_text()
                results.append(t)
                if len(results) == 3:
                    writer.writerow(results)
                    results = []

        if len(results) > 0:
            writer.writerow(results)

driver.quit()
