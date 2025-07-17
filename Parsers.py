import datetime
import lxml
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import HTMLTaker
import TechData
import UniDate
import LinkConst

def is_contains_work_keywords(text):
    keywords = ['работы','технич','технологич', 'недоступ', 'планов']
    if not text or not keywords:
        return False

    text = text.lower()
    keywords = [keyword.lower() for keyword in keywords]

    for keyword in keywords:
        if keyword in text:
            return True
    return False

def check_service_info(tech_data_list, temp_tech_data):
    if is_contains_work_keywords(temp_tech_data.work_header):
        tech_data_list.append(temp_tech_data)
    else:
        temp_tech_data.reset()

def parse_erip(service_name='service_name is null'):
    tech_data_list = []

    page_source = HTMLTaker.get_page_with_selenium(LinkConst.ERIP)
    if page_source is None:
        return

    soup = BeautifulSoup(page_source, "lxml")

    all_notif = soup.find_all('a', class_='news-item')
    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name

        if data.get('href') is not None:
            temp_tech_data.link = urljoin(LinkConst.ERIP, data.get('href'))

        date_span = data.find('span', class_='date')
        if date_span is not None:
            universal_date = UniDate.UniversalDate(date_span.text.strip())
            universal_date.parse_date_hard()
            temp_tech_data.publishing_date = universal_date.to_format()

        title_span = data.find('span', class_='news-title')
        if title_span is not None:
            temp_tech_data.description = title_span.text.strip()

        tech_data_list.append(temp_tech_data)
    return tech_data_list

def parse_BFT(service_name='service_name is null'):
    tech_data_list = []

    # Получаем HTML-код страницы через Selenium
    page_source = HTMLTaker.get_page_with_selenium(LinkConst.BFT)
    if page_source is None:
        return

    # Парсим HTML с помощью BeautifulSoup
    soup = BeautifulSoup(page_source, "lxml")

    all_notif = soup.find_all('div', class_='blog_post_preview rrrt format-standard')
    for data in all_notif:

        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name

        link_tag = data.find('a')
        if link_tag is not None and link_tag.get('href') is not None:
            temp_tech_data.link = urljoin(LinkConst.BFT, link_tag.get('href'))

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
    return tech_data_list

def parse_BPC(service_name = 'service_name is null'):
    tech_data_list = []
    page_source = HTMLTaker.get_page_with_selenium(LinkConst.BPC)
    if page_source is None:
        return

    soup = BeautifulSoup(page_source, "lxml")

    if soup is None:
        return

    all_notif = soup.find_all('div', class_='make_bet news_tab_item news-item s-5')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name

        link_tag = data.find('a')
        if link_tag is not None and link_tag.get('href') is not None:
            temp_tech_data.link =  urljoin(LinkConst.BPC, link_tag.get('href'))

        if data.find_all('div', class_='news_item_date') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('div', class_='news_item_date'))
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)

        if data.find_all('h3') is not None:
            temp_tech_data.work_header = data.find_all("h3")[0].text.strip()
            temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('h3'))

        if data.find_all('p', class_='preview-text') is not None:
            temp_tech_data.description = data.find_all('p', class_='preview-text')[0].text.strip()

        tech_data_list.append(temp_tech_data)

    return tech_data_list

def parse_MNS(service_name = 'service_name is null'):
    tech_data_list = []
    page_source = HTMLTaker.get_page_with_selenium(LinkConst.MNS)
    if page_source is None:
        return

    soup = BeautifulSoup(page_source, "lxml")

    if soup is None:
        return

    all_notif = soup.find_all('div', class_='latest-news row mx-n3 mt-n3')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name

        link_tag = data.find('a')
        if link_tag is not None and link_tag.get('href') is not None:
            temp_tech_data.link = urljoin(LinkConst.MNS, link_tag.get('href'))

        if data.find_all('div', class_='latest-news__date mb-2') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('div', class_='latest-news__date mb-2'))
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)

        if data.find_all('h3') is not None:
            temp_tech_data.work_header = data.find_all(class_="latest-news__title mb-4 d-block fs-20")[0].text.strip()
            # temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('h3'))

        tech_data_list.append(temp_tech_data)

    all_notif = soup.find_all('div', class_='item-list-news')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name

        link_tag = data.find('a')
        if link_tag is not None and link_tag.get('href') is not None:
            temp_tech_data.link =  urljoin(LinkConst.MNS, link_tag.get('href'))

        if data.find_all('div', class_='item-list-news__date mb-3') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('div', class_='item-list-news__date mb-3'))
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)

        if data.find_all('h3') is not None:
            temp_tech_data.work_header = data.find_all(class_="item-list-news__title h6 d-block mb-3")[0].text.strip()

        #temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('h3'))

        check_service_info(tech_data_list, temp_tech_data)

    return tech_data_list

def parse_OAIS(service_name = 'service_name is null'):
    tech_data_list = []
    page_source = HTMLTaker.get_page_with_selenium(LinkConst.OAIS)
    if page_source is None:
        return

    soup = BeautifulSoup(page_source, "lxml")

    if soup is None:
        return

    all_notif = soup.find_all('div', class_='su-post')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name

        link_tag = data.find('a')
        if link_tag is not None and link_tag.get('href') is not None:
            temp_tech_data.link =  urljoin(LinkConst.OAIS, link_tag.get('href'))

        if data.find_all('div', class_='su-post-meta') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('div', class_='su-post-meta'))
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)

        if data.find_all('strong') is not None:
            temp_tech_data.work_header = data.find_all("strong")[0].text.strip()

        if data.find_all('div', class_="su-post-excerpt") is not None:
            temp_tech_data.description = data.find_all('div', class_="su-post-excerpt")[0].text.strip()

        check_service_info(tech_data_list, temp_tech_data)

    return tech_data_list

def parse_A1(service_name = 'service_name is null'):
    tech_data_list = list()
    temp_tech_data = TechData.TechData()
    temp_tech_data.service_type = service_name
    temp_tech_data.work_header = "Работы каждый день, 99%"
    temp_tech_data.description = "Работы каждый день, 99%"
    temp_tech_data.link = LinkConst.A1
    current_date = datetime.datetime.now()
    temp_tech_data.publishing_date = current_date.strftime("%d.%m.%Y")
    temp_tech_data.date_of_work = current_date.strftime("%d.%m.%Y")
    tech_data_list.append(temp_tech_data)
    return tech_data_list

def parse_MTS(service_name = 'service_name is null'):
    tech_data_list = list()
    temp_tech_data = TechData.TechData()
    temp_tech_data.service_type = service_name
    temp_tech_data.work_header = "Работы каждый день, 99%"
    temp_tech_data.description = "Работы каждый день, 99%"
    temp_tech_data.link = LinkConst.MTS
    current_date = datetime.datetime.now()
    temp_tech_data.publishing_date = current_date.strftime("%d.%m.%Y")
    temp_tech_data.date_of_work = current_date.strftime("%d.%m.%Y")
    tech_data_list.append(temp_tech_data)
    return tech_data_list

def parse_Life(service_name = 'service_name is null'):
    tech_data_list = []
    page_source = HTMLTaker.get_page_with_selenium(LinkConst.Life)
    if page_source is None:
        return

    soup = BeautifulSoup(page_source, "lxml")

    if soup is None:
        return

    all_notif = soup.find_all('a', class_='NewsCard_link__j24Y5')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name

        if data is not None and data.get('href') is not None:
            temp_tech_data.link =  urljoin(LinkConst.Life, data.get('href'))

        if data.find_all('span', class_='NewsCard_date__ANy1J') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('span', class_='NewsCard_date__ANy1J'))
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)

        if data.find_all('h3', class_="NewsCard_title__ua0h4 m_8a5d1357") is not None:
            temp_tech_data.work_header = data.find_all('h3', class_="NewsCard_title__ua0h4 m_8a5d1357")[0].text.strip()
            temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('h3', class_="NewsCard_title__ua0h4 m_8a5d1357"))

        tech_data_list.append(temp_tech_data)

    return tech_data_list

def parse_Seventech(service_name = 'service_name is null'):
    tech_data_list = []
    page_source = HTMLTaker.get_page_with_selenium(LinkConst.Seventech)
    if page_source is None:
        return

    soup = BeautifulSoup(page_source, "lxml")

    if soup is None:
        return

    all_notif = soup.find_all('div', class_='elementor-post__card')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name

        link_tag = data.find('a')
        if link_tag is not None and link_tag.get('href') is not None:
            temp_tech_data.link =  urljoin(LinkConst.Seventech, link_tag.get('href'))

        if data.find_all('span', class_='elementor-post-date') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('span', class_='elementor-post-date'))
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)

        if data.find_all('h3') is not None:
            temp_tech_data.work_header = data.find_all("h3")[0].text.strip()
            temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('h3'))

        check_service_info(tech_data_list, temp_tech_data)

    return tech_data_list

def parse_Beltelecom(service_name = 'service_name is null'):
    tech_data_list = list()
    temp_tech_data = TechData.TechData()
    temp_tech_data.service_type = service_name
    temp_tech_data.work_header = "Работы каждый день, 90%"
    temp_tech_data.description = "Работы каждый день, 90%"
    temp_tech_data.link = LinkConst.Beltelecom
    current_date = datetime.datetime.now()
    temp_tech_data.publishing_date = current_date.strftime("%d.%m.%Y")
    temp_tech_data.date_of_work = current_date.strftime("%d.%m.%Y")
    tech_data_list.append(temp_tech_data)
    return tech_data_list

def parse_Delova9Seti(service_name = 'service_name is null'):
    tech_data_list = []
    page_source = HTMLTaker.get_page_with_selenium(LinkConst.Delova9Seti)
    if page_source is None:
        return

    soup = BeautifulSoup(page_source, "lxml")

    if soup is None:
        return

    all_notif = soup.find_all('div', class_='card y_2025 col-md-4 col-sm-6 col-12')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name

        link_tag = data.find('a')
        if link_tag is not None and link_tag.get('href') is not None:
            temp_tech_data.link =  urljoin(LinkConst.Delova9Seti, link_tag.get('href'))

        if data.find_all('p', class_='text-small text-gray mb-4') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('p', class_='text-small text-gray mb-4'))
            try:
                temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)
            except:
                temp_tech_data.publishing_date = ""

        if data.find_all('h2') is not None:
            temp_tech_data.work_header = data.find_all("h2")[0].text.strip()
            temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('h2'))

        if data.find_all('a', class_='card-link') is not None:
            temp_tech_data.description =' '.join(data.find_all('a', class_='card-link')[0].text.strip().split())

        tech_data_list.append(temp_tech_data)

    return tech_data_list

def parse_Hoster(service_name = 'service_name is null'):
    tech_data_list = []
    page_source = HTMLTaker.get_page_with_selenium(LinkConst.Hoster)
    if page_source is None:
        return

    soup = BeautifulSoup(page_source, "lxml")

    if soup is None:
        return

    all_notif = soup.find_all('a', class_='m-mediacenter-item')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name

        if data is not None and data.get('href') is not None:
            temp_tech_data.link =  urljoin(LinkConst.Hoster, data.get('href'))

        if data.find_all('span', class_='m-mediacenter-item-date m-font-b2') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('span', class_='m-mediacenter-item-date m-font-b2'))
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)

        if data.find_all('span',class_="m-mediacenter-item-title m-font-hl4") is not None:
            header_tags = data.select('span[class^="m-mediacenter-item-title"]')
            if header_tags:
                temp_tech_data.work_header = header_tags[0].text.strip()
            else:
                print("Заголовок не найден.")
            temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(temp_tech_data.work_header)

        check_service_info(tech_data_list, temp_tech_data)

    return tech_data_list

def parse_BeCloud(service_name = 'service_name is null'):
    tech_data_list = []
    page_source = HTMLTaker.get_page_with_selenium(LinkConst.BeCloud)
    if page_source is None:
        return

    soup = BeautifulSoup(page_source, "lxml")

    if soup is None:
        return

    all_notif = soup.find_all('div', class_='news__item')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name

        link_tag = data.find('a')
        if link_tag is not None and link_tag.get('href') is not None:
            temp_tech_data.link =  urljoin(LinkConst.BeCloud, link_tag.get('href'))

        if data.find_all('div', class_='news-date') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('div', class_='news-date'))
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)

        if data.find_all('h6') is not None:
            temp_tech_data.work_header = data.find_all("h6")[0].text.strip()
            temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('h6'))

        check_service_info(tech_data_list, temp_tech_data)

    return tech_data_list

def parse_Oplati(service_name = 'service_name is null'):
    tech_data_list = []
    page_source = HTMLTaker.get_page_with_selenium(LinkConst.Oplati)
    if page_source is None:
        return

    soup = BeautifulSoup(page_source, "lxml")

    if soup is None:
        return

    all_notif = soup.find_all('section', class_='opacity')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name

        link_tag = data.find('a')
        if link_tag is not None and link_tag.get('href') is not None:
            temp_tech_data.link =  urljoin(LinkConst.Oplati, link_tag.get('href'))

        if data.find_all('div', class_='data') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('div', class_='data'))
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)

        if data.find_all('h1') is not None:
            temp_tech_data.work_header = data.find_all("h1")[0].text.strip()
            temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('h1'))

        check_service_info(tech_data_list, temp_tech_data)

    return tech_data_list
