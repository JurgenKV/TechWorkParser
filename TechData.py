from urllib.parse import urljoin


class TechData:
    service_type = ''
    publishing_date = ''
    date_of_work = ''
    work_header = ''
    description = ''
    link = ''

    def __init__(self, service_name = ''):
        service_type = service_name
        publishing_date = ''
        date_of_work = ''
        work_header = ''
        description = ''
        link = ''

    def reset(self):
        service_type = ''
        publishing_date = ''
        date_of_work = ''
        work_header = ''
        description = ''
        link = ''
        # for data in all_notif:
        #     if data.find_all('div', class_='news_item_date') is not None:
        #         universal_date = UniDate.UniversalDate(data.find_all('div', class_='news_item_date'))
        #         temp_tech_data.publishing_date = UniDate.UniversalDate.parse_date_from_text(universal_date.date_string)
        #     # Заголовок новости и дата планируемой тех. работы(если есть в адекватном формате)
        #     if data.find_all('h3') is not None:
        #         temp_tech_data.work_header = data.find_all("h3")[0].text.strip()
        #         temp_tech_data.date_of_work = UniDate.UniversalDate.parse_date_from_text(data.find_all('h3'))
        #     # Описание новости (если есть)
        #     if data.find_all('p', class_='preview-text') is not None:
        #         temp_tech_data.description = data.find_all('p', class_='preview-text')[0].text.strip()

    @staticmethod
    def get_news_link_from_tag(temp_tech_data, data, link , data_find_tag, get_tag ):
        try:
            link_tag = data.find(data_find_tag)
            if link_tag is not None and link_tag.get(get_tag) is not None:
                temp_tech_data.link = urljoin(link, link_tag.get(get_tag))
        except Exception as e:
            print(e)
            temp_tech_data.link = 'Error get_news_link_from_tag'
        return temp_tech_data

    def get_news_link_from_data(temp_tech_data, data, link, get_tag ):
        try:
            if data is not None and data.get(get_tag) is not None:
                temp_tech_data.link = urljoin(link, data.get(get_tag))
        except Exception as e:
            print(e)
            temp_tech_data.link = 'Error get_news_link_from_tag'
        return temp_tech_data