import datetime
import re

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

def parse_ERIP(service_name='service_name is null'):
    tech_data_list = []
    soup = HTMLTaker.get_soup_page(LinkConst.ERIP, 'lxml')
    if soup is None:
        return

    all_notif = soup.find_all('a', class_='news-item swiper-slide swiper-slide-active')
    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name
        # Ссылка на новость
        if data is not None and data.get('href') is not None:
            temp_tech_data.link = urljoin(LinkConst.ERIP, data.get('href'))
        # Дата публикации
        if data.find_all('span', class_='date') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('span', class_='date')[0].text.strip())
            universal_date.parse_date_hard()
            temp_tech_data.publishing_date = universal_date.to_format()

        # Заголовок новости и дата планируемой тех. работы(если есть в адекватном формате)
        if data.find_all('span', class_='news-title') is not None:
            temp_tech_data.work_header = data.find_all('span', class_='news-title')[0].text.strip()
            temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('span', class_='news-title'))

        tech_data_list.append(temp_tech_data)
    return tech_data_list

def parse_BFT(service_name='service_name is null'):
    tech_data_list = []

    soup = HTMLTaker.get_soup_page(LinkConst.BFT, 'lxml')
    if soup is None:
        return

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

        check_service_info(tech_data_list, temp_tech_data)
    return tech_data_list
# gold template
def parse_BPC(service_name = 'service_name is null'):
    tech_data_list = []
    soup = HTMLTaker.get_soup_page(LinkConst.BPC, 'lxml')
    if soup is None:
        return

    # item новости
    all_notif = soup.find_all('div', class_='make_bet news_tab_item news-item s-5')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name
        # Ссылка на новость
        link_tag = data.find('a')
        if link_tag is not None and link_tag.get('href') is not None:
            temp_tech_data.link =  urljoin(LinkConst.BPC, link_tag.get('href'))
        # Дата публикации
        if data.find_all('div', class_='news_item_date') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('div', class_='news_item_date'))
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)
        # Заголовок новости и дата планируемой тех. работы(если есть в адекватном формате)
        if data.find_all('h3') is not None:
            temp_tech_data.work_header = data.find_all("h3")[0].text.strip()
            temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('h3'))
        # Описание новости (если есть)
        if data.find_all('p', class_='preview-text') is not None:
            temp_tech_data.description = data.find_all('p', class_='preview-text')[0].text.strip()

        check_service_info(tech_data_list, temp_tech_data)

    return tech_data_list

def parse_MNS(service_name = 'service_name is null'):
    tech_data_list = []
    soup = HTMLTaker.get_soup_page(LinkConst.MNS, 'lxml')
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
    soup = HTMLTaker.get_soup_page(LinkConst.OAIS, 'lxml')
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
    soup = HTMLTaker.get_soup_page(LinkConst.Life, 'lxml')
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
    soup = HTMLTaker.get_soup_page(LinkConst.Seventech, 'lxml')
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
    soup = HTMLTaker.get_soup_page(LinkConst.Delova9Seti, 'lxml')
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
    soup = HTMLTaker.get_soup_page(LinkConst.Hoster, 'lxml')
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
    soup = HTMLTaker.get_soup_page(LinkConst.BeCloud, 'lxml')
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
    soup = HTMLTaker.get_soup_page(LinkConst.Oplati, 'lxml')
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

def parse_Kupala(service_name = 'service_name is null'):
    tech_data_list = []
    soup = HTMLTaker.get_soup_page(LinkConst.Kupala, 'lxml')
    if soup is None:
        return

    all_notif = soup.find_all('div', class_='news-item js-hover')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name

        link_tag = data.find('a')
        if link_tag is not None and link_tag.get('href') is not None:
            temp_tech_data.link =  urljoin(LinkConst.Kupala, link_tag.get('href'))

        if data.find_all('div', class_='date') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('div', class_='date'))
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)

        if data.find_all('a', class_="title js-lnk") is not None:
            temp_tech_data.work_header = data.find_all('a', class_="title js-lnk")[0].text.strip()
            temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('a', class_="title js-lnk"))

        check_service_info(tech_data_list, temp_tech_data)

    return tech_data_list

def parse_BVFB(service_name = 'service_name is null'):
    tech_data_list = []
    soup = HTMLTaker.get_soup_page(LinkConst.BVFB, 'lxml')
    if soup is None:
        return

    # item новости
    all_notif = soup.find_all('div', class_='pl-0 col-12 col-sm-6 col-md-4 py-3 bb_dark_line d-flex flex-column justify-content-between')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name
        # Ссылка на новость
        link_tag = data.find('a')
        if link_tag is not None and link_tag.get('href') is not None:
            temp_tech_data.link =  urljoin(LinkConst.BVFB, link_tag.get('href'))
        # Дата публикации
        if data.find_all('small', class_='text-muted') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('small', class_='text-muted'))
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)
        # Заголовок новости и дата планируемой тех. работы(если есть в адекватном формате)
        if data.find_all('a', class_='text-pc font-weight-bold proxima-nova fs-16 mb-2') is not None:
            temp_tech_data.work_header = data.find_all('a', class_='text-pc font-weight-bold proxima-nova fs-16 mb-2')[0].text.strip()
            temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('a', class_='text-pc font-weight-bold proxima-nova fs-16 mb-2'))

        check_service_info(tech_data_list, temp_tech_data)

    return tech_data_list

def parse_NBRB(service_name = 'service_name is null'):
    tech_data_list = []
    soup = HTMLTaker.get_soup_page(LinkConst.NBRB, 'lxml')
    if soup is None:
        return

    # item новости
    all_notif = soup.find_all('article', class_='n-article')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name
        # Ссылка на новость
        link_tag = data.find('a')
        if link_tag is not None and link_tag.get('href') is not None:
            temp_tech_data.link =  urljoin(LinkConst.NBRB, link_tag.get('href'))
        # Дата публикации
        if data.find_all('div', class_='n-date') is not None:
            try:
                text_date = data.find_all('div', class_='n-date')[0].text.split()
                universal_date = UniDate.UniversalDate(f'{text_date[2]} {text_date[0]} {text_date[1]}')
                universal_date.parse_date_hard()
                temp_tech_data.publishing_date = universal_date.to_format()
            except IndexError:
                print()
        # Заголовок новости и дата планируемой тех. работы(если есть в адекватном формате)
        if data.find_all('div', class_='pub__descr') is not None:
            try:
                temp_tech_data.work_header = data.find_all('div', class_='pub__descr')[0].text.strip()
                temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('div', class_='pub__descr'))
            except Exception as e:
                print(e)

        check_service_info(tech_data_list, temp_tech_data)

    return tech_data_list

def parse_Bank_AlfaRu(service_name = 'service_name is null'):
    tech_data_list = []
    soup = HTMLTaker.get_soup_page(LinkConst.Bank_AlfaRu, 'lxml')
    if soup is None:
        return

    # item новости
    all_notif = soup.find_all('li', class_='dLBOHl bLBOHl hLBOHl')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name
        # Ссылка на новость
        link_tag = data.find('a')
        if link_tag is not None and link_tag.get('href') is not None:
            temp_tech_data.link =  urljoin(LinkConst.Bank_AlfaRu, link_tag.get('href'))
        # Дата публикации
        if data.find_all('span', class_='aR7Oy1 bR7Oy1 vR7Oy1 RR7Oy1 hR7Oy1 GQWkTE aIrO76') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('span', class_='aR7Oy1 bR7Oy1 vR7Oy1 RR7Oy1 hR7Oy1 GQWkTE aIrO76'))
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)
        # Заголовок новости и дата планируемой тех. работы(если есть в адекватном формате)
        if data.find_all('h3', class_='aR7Oy1 yR7Oy1 MR7Oy1 UR7Oy1 nQWkTE CQWkTE RQWkTE _5QWkTE dLBOHl eLBOHl') is not None:
            temp_tech_data.work_header = data.find_all("h3", class_='aR7Oy1 yR7Oy1 MR7Oy1 UR7Oy1 nQWkTE CQWkTE RQWkTE _5QWkTE dLBOHl eLBOHl')[0].text.strip()
            temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('h3', class_='aR7Oy1 yR7Oy1 MR7Oy1 UR7Oy1 nQWkTE CQWkTE RQWkTE _5QWkTE dLBOHl eLBOHl'))
        check_service_info(tech_data_list, temp_tech_data)

    return tech_data_list

def parse_Bank_Belarusbank(service_name = 'service_name is null'):
    tech_data_list = []
    soup = HTMLTaker.get_soup_page(LinkConst.Bank_Belarusbank, 'lxml')
    if soup is None:
        return

    # item новости
    all_notif = soup.find_all('div', class_='article-grid__item col col-lg-12')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name
        # Ссылка на новость
        link_tag = data.find('a')
        if link_tag is not None and link_tag.get('href') is not None:
            temp_tech_data.link =  urljoin(LinkConst.Bank_Belarusbank, link_tag.get('href'))
        # Дата публикации
        if data.find_all('div', class_='status-label') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('div', class_='status-label'))
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)
        # Заголовок новости и дата планируемой тех. работы(если есть в адекватном формате)
        if data.find_all('span', class_='link') is not None:
            temp_tech_data.work_header = data.find_all('span', class_='link')[0].text.strip()
            temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('span', class_='link'))

        check_service_info(tech_data_list, temp_tech_data)

    return tech_data_list

def parse_Bank_BSB(service_name = 'service_name is null'):
    tech_data_list = []
    soup = HTMLTaker.get_soup_page(LinkConst.Bank_BSB, 'lxml')
    if soup is None:
        return

    # item новости
    all_notif = soup.find_all('div', class_='news-card__item')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name
        # Ссылка на новость
        link_tag = data.find('a')
        if link_tag is not None and link_tag.get('href') is not None:
            temp_tech_data.link =  urljoin(LinkConst.Bank_BSB, link_tag.get('href'))
        # Дата публикации
        if data.find_all('div', class_='gray-color') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('div', class_='gray-color'))
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)
        # Заголовок новости и дата планируемой тех. работы(если есть в адекватном формате)
        if data.find_all('div', class_='font-24') is not None:
            temp_tech_data.work_header = data.find_all('div', class_='font-24')[0].text.strip()
            temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('div', class_='font-24'))

        check_service_info(tech_data_list, temp_tech_data)

    return tech_data_list

def parse_Bank_BTA(service_name = 'service_name is null'):
    tech_data_list = []
    soup = HTMLTaker.get_soup_page(LinkConst.Bank_BTA, 'lxml')
    if soup is None:
        return

    # item новости
    all_notif = soup.find_all('div', class_='news-grid__item')

    for data in all_notif:
        try:
            temp_tech_data = TechData.TechData()
            temp_tech_data.service_type = service_name
            # Ссылка на новость
            link_tag = data.find('a')
            if link_tag is not None and link_tag.get('href') is not None:
                temp_tech_data.link =  urljoin(LinkConst.Bank_BTA, link_tag.get('href'))
            # Дата публикации
            if data.find_all('span', class_='news-card__date') is not None:
                universal_date = UniDate.UniversalDate(data.find_all('span', class_='news-card__date'))
                temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)
            # Заголовок новости и дата планируемой тех. работы(если есть в адекватном формате)
            if data.find_all('div', class_='news-card__title') is not None:
                temp_tech_data.work_header = data.find_all('div', class_='news-card__title')[0].text.strip()
                temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('div', class_='news-card__title'))
            check_service_info(tech_data_list, temp_tech_data)
        except Exception as e:
            print(e)

    return tech_data_list

def parse_Bank_BankReshenii(service_name = 'service_name is null'):
    tech_data_list = []
    soup = HTMLTaker.get_soup_page(LinkConst.Bank_BankReshenii, 'lxml')
    if soup is None:
        return

    # item новости
    all_notif = soup.find_all('div', class_='page-promotion__item')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name
        # Ссылка на новость
        link_tag = data.find('a')
        if link_tag is not None and link_tag.get('href') is not None:
            temp_tech_data.link =  urljoin(LinkConst.Bank_BankReshenii, link_tag.get('href'))
        # Дата публикации
        if data.find_all('div', class_='tag-label') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('div', class_='tag-label'))
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)
        # Заголовок новости и дата планируемой тех. работы(если есть в адекватном формате)
        if data.find_all('div', class_='card-sale__title') is not None:
            temp_tech_data.work_header = data.find_all('div', class_='card-sale__title')[0].text.strip()
            temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('div', class_='card-sale__title'))
        check_service_info(tech_data_list, temp_tech_data)

    return tech_data_list

def parse_Bank_BELWEB(service_name = 'service_name is null'):
    tech_data_list = []
    soup = HTMLTaker.get_soup_page(LinkConst.Bank_BELWEB, 'lxml')
    if soup is None:
        return

    # item новости
    all_notif = soup.find_all('div', class_='card-elem__inner')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name
        # Ссылка на новость
        link_tag = data.find('a')
        if link_tag is not None and link_tag.get('href') is not None:
            temp_tech_data.link =  urljoin(LinkConst.Bank_BELWEB, link_tag.get('href'))
        # Дата публикации
        if data.find_all('div', class_='card__text-desc') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('div', class_='card__text-desc'))
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)
        # Заголовок новости и дата планируемой тех. работы(если есть в адекватном формате)
        if data.find_all('div', class_='card__text-context') is not None:
            temp_tech_data.work_header = data.find_all('div', class_='card__text-context')[0].text.strip()
            temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('div', class_='card__text-context'))

        check_service_info(tech_data_list, temp_tech_data)

    return tech_data_list

def parse_Bank_BelAgro(service_name = 'service_name is null'):
    tech_data_list = []
    soup = HTMLTaker.get_soup_page(LinkConst.Bank_BelAgro, 'lxml')
    if soup is None:
        return

    # item новости
    all_notif = soup.find_all('div', class_='news-catalog__item news-catalog__item--lg')
    all_notif += soup.find_all('a', href= [re.compile(r'^/about/press-tsentr/novosti/'), ''] )
    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name
        # Ссылка на новость

        if data is not None and data.get('href') is not None:
            temp_tech_data.link =  urljoin(LinkConst.Bank_BelAgro, data.get('href'))
            if temp_tech_data.link is None:
                try:
                    link_tag = data.find('a', class_='btn btn-full')
                    if link_tag is not None and link_tag.get('href') is not None:
                        temp_tech_data.link = urljoin(LinkConst.Bank_BELWEB, link_tag.get('href'))
                except Exception as e:
                    pass

        # Дата публикации
        if data.find_all('div', class_='data') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('div', class_='data'))
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)

        # Заголовок новости и дата планируемой тех. работы(если есть в адекватном формате)
        if data.find_all('div', class_='h4') is not None:
            try:
                temp_tech_data.work_header = data.find_all('div', class_='h4')[0].text.strip()
                temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('div', class_='h4'))
            except Exception as e:
                pass
            try:
                temp_tech_data.work_header = data.find_all("p")[0].text.strip()
                temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('p'))
            except Exception as e:
                pass
                try:
                    temp_tech_data.work_header = data.find_all("h4")[0].text.strip()
                    temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('h4'))
                except Exception as e:
                    pass

        tech_data_list.append(temp_tech_data)
        check_service_info(tech_data_list, temp_tech_data)

    return tech_data_list

def parse_Bank_Belinvest(service_name = 'service_name is null'):
    tech_data_list = []
    soup = HTMLTaker.get_soup_page(LinkConst.Bank_Belinvest, 'lxml')
    if soup is None:
        return

    # item новости
    all_notif = soup.find_all('div', class_='press-newsList-item')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name
        # Ссылка на новость
        link_tag = data.find('a')
        if link_tag is not None and link_tag.get('href') is not None:
            temp_tech_data.link =  urljoin(LinkConst.Bank_Belinvest, link_tag.get('href'))
        # Дата публикации
        if data.find_all('span', class_='date openSansSemiBold') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('span', class_='date openSansSemiBold'))
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)
        # Заголовок новости и дата планируемой тех. работы(если есть в адекватном формате)
        if data.find_all('a', class_='item-h3 openSansRegular') is not None:
            temp_tech_data.work_header = data.find_all('a', class_='item-h3 openSansRegular')[0].text.strip()
            temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('a', class_='item-h3 openSansRegular'))
        # Описание новости (если есть)
        if data.find_all('p', class_='item-p openSansRegular dots completed') is not None:
            temp_tech_data.description = data.find_all('p', class_='item-p openSansRegular dots completed')[0].text.strip()

        check_service_info(tech_data_list, temp_tech_data)

    return tech_data_list

def parse_Bank_MTB(service_name = 'service_name is null'):
    tech_data_list = []
    soup = HTMLTaker.get_soup_page(LinkConst.Bank_MTB, 'lxml')
    if soup is None:
        return

    # item новости
    all_notif = soup.find_all('article', class_='news-article')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name
        # Ссылка на новость
        link_tag = data.find('a')
        if link_tag is not None and link_tag.get('href') is not None:
            temp_tech_data.link =  urljoin(LinkConst.Bank_MTB, link_tag.get('href'))
        # Дата публикации
        if data.find_all('time', class_='news-article__time') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('time', class_='news-article__time'))
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)
        # Заголовок новости и дата планируемой тех. работы(если есть в адекватном формате)
        if data.find_all('span',class_='news-article__title') is not None:

                temp_tech_data.work_header = data.find_all('span',class_="news-article__title")[0].text.strip()
                temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('span',class_='news-article__title'))

        # Описание новости (если есть)
        if data.find_all('p', class_='news-article__text') is not None:
            temp_tech_data.description = data.find_all('p', class_='news-article__text')[0].text.strip()

        check_service_info(tech_data_list, temp_tech_data)

    return tech_data_list

def parse_Bank_Paritet(service_name = 'service_name is null'):
    tech_data_list = []
    soup = HTMLTaker.get_soup_page(LinkConst.Bank_Paritet, 'lxml')
    if soup is None:
        return

    # item новости
    all_notif = soup.find_all('a', class_='news__item')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name
        # Ссылка на новость

        if data is not None and data.get('href') is not None:
            temp_tech_data.link =  urljoin(LinkConst.Bank_Paritet, data.get('href'))
        # Дата публикации
        if data.find_all('div', class_='news__date') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('div', class_='news__date'))
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)
        # Заголовок новости и дата планируемой тех. работы(если есть в адекватном формате)
        if data.find_all('p') is not None:
            try:
                temp_tech_data.work_header = data.find_all("p")[0].text.strip()
                temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('p'))
            except Exception as e:
                pass
        check_service_info(tech_data_list, temp_tech_data)

    return tech_data_list

def parse_Bank_Zepter(service_name = 'service_name is null'):
    tech_data_list = []
    soup = HTMLTaker.get_soup_page(LinkConst.Bank_Zepter, 'lxml')
    if soup is None:
        return

    # item новости
    all_notif = soup.find_all('div', class_='row row_col_2')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name
        # Ссылка на новость
        link_tag = data.find('a')
        if link_tag is not None and link_tag.get('href') is not None:
            temp_tech_data.link =  urljoin(LinkConst.Bank_Zepter, link_tag.get('href'))
        # Дата публикации
        if data.find_all('div', class_='rc_title') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('div', class_='rc_title'))
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)
        # Заголовок новости и дата планируемой тех. работы(если есть в адекватном формате)
        if data.find_all('span', class_='undecor') is not None:
            temp_tech_data.work_header = data.find_all('span', class_='undecor')[0].text.strip()
            temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('span', class_='undecor'))

        check_service_info(tech_data_list, temp_tech_data)

    return tech_data_list

def parse_Bank_Sberbank(service_name = 'service_name is null'):
    tech_data_list = []
    soup = HTMLTaker.get_soup_page(LinkConst.Bank_Sberbank, 'lxml')
    if soup is None:
        return
    # item новости
    all_notif = soup.find_all('a', class_='NewsFeedElement')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name
        # Ссылка на новость
        if data is not None and data.get('href') is not None:
            temp_tech_data.link = urljoin(LinkConst.Bank_Sberbank, data.get('href'))
        # Дата публикации
        if data.find_all('div', class_='NewsFeedElement__data') is not None:
            date = data.find_all('div', class_='NewsFeedElement__data')[0].text.strip()
            date = date +' '+ str(datetime.datetime.now().year)
            universal_date = UniDate.UniversalDate(date)
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)
        # Заголовок новости и дата планируемой тех. работы(если есть в адекватном формате)
        if data.find_all('div', class_='NewsFeedElement__title') is not None:
            temp_tech_data.work_header = data.find_all('div', class_='NewsFeedElement__title')[0].text.strip()
            temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(
                data.find_all('div', class_='NewsFeedElement__title'))

        tech_data_list.append(temp_tech_data)
        check_service_info(tech_data_list, temp_tech_data)

    return tech_data_list

def parse_Bank_Priorbank(service_name = 'service_name is null'):
    tech_data_list = []
    soup = HTMLTaker.get_soup_page(LinkConst.Bank_Priorbank, 'lxml')
    if soup is None:
        return
    # item новости
    all_notif = soup.find_all('div', class_='news-list__item')

    for data in all_notif:
        temp_tech_data = TechData.TechData()
        temp_tech_data.service_type = service_name
        # Ссылка на новость
        link_tag = data.find('a')
        if link_tag is not None and link_tag.get('href') is not None:
            temp_tech_data.link =  urljoin(LinkConst.Bank_Priorbank, link_tag.get('href'))
        # Дата публикации
        if data.find_all('span') is not None:
            universal_date = UniDate.UniversalDate(data.find_all('span'))
            temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)
        # Заголовок новости и дата планируемой тех. работы(если есть в адекватном формате)
        if data.find_all('a',class_='news-list__title-link') is not None:
            temp_tech_data.work_header = data.find_all('a',class_="news-list__title-link")[0].text.strip()
            temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('a',class_='news-list__title-link'))

        check_service_info(tech_data_list, temp_tech_data)

    return tech_data_list
