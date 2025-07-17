import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import TechData
import UniDate
import LinkConst

HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive"
    }

# Настройки для Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Запуск в фоновом режиме (без GUI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")


def initialize_driver():
    service = Service("C:\\Soft\\chromedriver\\chromedriver.exe")  # Укажите путь к chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def get_page_with_selenium(url, timeout=10):
    try:
        driver = initialize_driver()
        driver.get(url)

        # Ждём, пока страница полностью загрузится
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Возвращаем HTML-код страницы
        page_source = driver.page_source
        driver.quit()
        return page_source

    except Exception as e:
        print("Ошибка при загрузке страницы:", e)
        return None

def get_request(link, service_name):
    try:
        response = requests.get(LinkConst.ERIP, headers=HEADERS, timeout=10)  # Добавлен таймаут
        response.raise_for_status()  # Проверка на HTTP-ошибки
        return BeautifulSoup(response.content, "lxml")

    except requests.exceptions.RequestException as e:
        print("Ошибка при выполнении запроса:", e)
        return None
    except Exception as e:
        print("Неизвестная ошибка:", e)
        return None


def parse_erip(service_name='service_name is null'):
    all_notif = []
    tech_data_list = []

    # Получаем HTML-код страницы через Selenium
    page_source = get_page_with_selenium(LinkConst.ERIP)
    if page_source is None:
        return

    # Парсим HTML с помощью BeautifulSoup
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page_source, "lxml")

    all_notif = soup.find_all('a', class_='news-item')
    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name

        if data.get('href') is not None:
            temp_tech_data.link = data.get('href')

        date_span = data.find('span', class_='date')
        if date_span is not None:
            universal_date = UniDate.UniversalDate(date_span.text.strip())
            universal_date.parse_date_hard()
            temp_tech_data.publishing_date = universal_date.to_format()

        title_span = data.find('span', class_='news-title')
        if title_span is not None:
            temp_tech_data.description = title_span.text.strip()

        tech_data_list.append(temp_tech_data)

    print("Отфильтрованные уведомления:")
    for notif in tech_data_list:
        print(notif.service_type)
        print(notif.date_of_work)
        print(notif.publishing_date)
        print(notif.link)
        print(notif.description)
        print('-------------------')

    return tech_data_list

# def parse_erip(service_name = 'service_name is null'):
#     all_notif = []
#     filtered_notif = []
#     tech_data_list = []
#
#     soup = get_request(LinkConst.ERIP, service_name)
#     if soup is None:
#         return
#
#     all_notif = soup.find_all('a', class_='news-item')
#     #     service_type = ''
#     #     publishing_date = ''
#     #     date_of_work = ''
#     #     description = ''
#     #     link = ''
#     for data in all_notif:
#         temp_tech_data = TechData.TechData()
#         temp_tech_data.service_type = service_name
#
#         if data.get('href') is not None:
#                temp_tech_data.link = data.get('href')
#
#         if data.find_all('span', class_='date') is not None:
#             universal_date = UniDate.UniversalDate(data.find_all('span', class_='date')[0].text.strip())
#             universal_date.parse_date_hard()
#             temp_tech_data.publishing_date = universal_date.to_format()
#
#         if data.find_all('span', class_='news-title') is not None:
#             temp_tech_data.description = data.find_all('span', class_='news-title')[0].text.strip()
#
#         tech_data_list.append(temp_tech_data)
#
#     print("Отфильтрованные уведомления:")
#     for notif in tech_data_list:
#         print(notif.service_type)
#         print(notif.date_of_work)
#         print(notif.publishing_date)
#         print(notif.link)
#         print(notif.description)
#         print('-------------------')
#
#     return tech_data_list


def parse_BFT(service_name='service_name is null'):
    all_notif = []
    tech_data_list = []

    # Получаем HTML-код страницы через Selenium
    page_source = get_page_with_selenium(LinkConst.BFT)
    if page_source is None:
        return

    # Парсим HTML с помощью BeautifulSoup
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page_source, "lxml")

    all_notif = soup.find_all('div', class_='blog_post_preview rrrt format-standard')
    for data in all_notif:

        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name

        link_tag = data.find('a')
        if link_tag is not None and link_tag.get('href') is not None:
            temp_tech_data.link = link_tag.get('href')

        date_span = data.find('span', class_='post_date')
        if date_span is not None:
            universal_date = UniDate.UniversalDate(date_span.text.strip())
            universal_date.parse_date_hard()
            temp_tech_data.publishing_date = universal_date.to_format()

        date_span = data.find('h2', class_='blogpost_title')
        if date_span is not None:
            temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(date_span.text)

        title_span = data.find('p')
        if title_span is not None:
            temp_tech_data.description = title_span.text.strip()

        tech_data_list.append(temp_tech_data)

    print("Отфильтрованные уведомления:")
    for notif in tech_data_list:
        print(notif.service_type)
        print(notif.date_of_work)
        print(notif.publishing_date)
        print(notif.link)
        print(notif.description)
        print('-------------------')

    return tech_data_list


def parse_BPC(service_name = 'service_name is null'):
    all_notif = []
    filtered_notif = []
    tech_data_list = []

    page_source = get_page_with_selenium(LinkConst.BPC)
    if page_source is None:
        return

    soup = BeautifulSoup(page_source, "lxml")

    if soup is None:
        return

    all_notif = soup.find_all('div', class_='make_bet news_tab_item news-item s-5')
    #     service_type = ''
    #     publishing_date = ''
    #     date_of_work = ''
    #     description = ''
    #     link = ''
    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name

        link_tag = data.find('a')
        if link_tag is not None and link_tag.get('href') is not None:
            temp_tech_data.link = link_tag.get('href')

        if data.find_all('div', class_='news_item_date') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('div', class_='news_item_date'))
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)

        if data.find_all('h3') is not None:
            temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('h3'))

        if data.find_all('p', class_='preview-text') is not None:
            temp_tech_data.description = data.find_all('p', class_='preview-text')[0].text.strip()

        tech_data_list.append(temp_tech_data)

    print("Отфильтрованные уведомления:")
    for notif in tech_data_list:
        print(notif.service_type)
        print(notif.date_of_work)
        print(notif.publishing_date)
        print(notif.link)
        print(notif.description)
        print('-------------------')

    return tech_data_list

