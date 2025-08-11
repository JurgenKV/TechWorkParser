import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import LOG

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
chrome_options.add_argument("--enable-unsafe-swiftshader")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-webgl")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

WEB_DRIVER: WebDriver

def initialize_driver():
    try:
        f = open('ChromeDriver_path.txt', 'r')
        service = Service(f.readline().strip())  # Укажите путь к chromedriver
        f.close()
    except Exception as e:
        print(e)
        LOG.error(str(e))
    global WEB_DRIVER
    WEB_DRIVER = webdriver.Chrome(service=service, options=chrome_options)

def quit_driver():
    WEB_DRIVER.quit()

def get_page_with_selenium(url, timeout=20):
    try:
        #driver = initialize_driver()
        WEB_DRIVER.get(url)

        # Ждём, пока страница полностью загрузится
        WebDriverWait(WEB_DRIVER, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Возвращаем HTML-код страницы
        page_source = WEB_DRIVER.page_source
        #WEB_DRIVER.quit()
        return page_source

    except Exception as e:
        LOG.error("Ошибка при загрузке страницы:" + str(e))
        print("Ошибка при загрузке страницы:", e)
        return None

def get_request(link, service_name):
    try:
        response = requests.get(link, headers=HEADERS, timeout=10)  # Добавлен таймаут
        response.raise_for_status()  # Проверка на HTTP-ошибки
        return BeautifulSoup(response.content, "lxml")

    except requests.exceptions.RequestException as e:
        print(f"{service_name} Ошибка при выполнении запроса:", e)
        LOG.error(f"{service_name} Ошибка при выполнении запроса:" + str(e))
        return None
    except Exception as e:
        LOG.error(f"{service_name} Неизвестная ошибка:" + str(e))
        print(f" {service_name} Неизвестная ошибка:", e)
        return None

def get_soup_page(link, soup_features = 'lxml'):
    soup = None
    try:
        page_source = get_page_with_selenium(link)
        if page_source is None:
            print(f'{link} page_source is null')
            LOG.error(f'{link} page_source is null')
            return
        soup = BeautifulSoup(page_source, soup_features)
    except Exception as e:
        print(e)
        LOG.error(f'{str(e)}')
    if soup is None:
        print(f'{link} soup is null')
        LOG.error(f'{link} soup is null')
    return soup
