import Parsers
from TechData import TechData

if __name__ == '__main__':
    all_tech_list = list()
    #all_tech_list.extend(Parsers.parse_erip('ERIP'))
    #all_tech_list.extend(Parsers.parse_BFT('BFT'))
    #all_tech_list.extend(Parsers.parse_BPC('BPC'))
    #all_tech_list.extend(Parsers.parse_MNS('MNS'))
    #all_tech_list.extend(Parsers.parse_OAIS('OAIS'))
    #all_tech_list.extend(Parsers.parse_A1('A1')) # cringo
    #all_tech_list.extend(Parsers.parse_MTS('MTS')) # cringo
    #all_tech_list.extend(Parsers.parse_Life('Life'))
    #all_tech_list.extend(Parsers.parse_Seventech('Seventech'))
    #all_tech_list.extend(Parsers.parse_Beltelecom('Beltelecom')) # cringo
    #all_tech_list.extend(Parsers.parse_Delova9Seti('Деловая Сеть'))
    #all_tech_list.extend(Parsers.parse_Hoster('Hoster'))
    #all_tech_list.extend(Parsers.parse_BeCloud('BeCloud'))
    #all_tech_list.extend(Parsers.parse_Oplati('Oplati'))

    for notif in all_tech_list:
        print(f"Сервис: {notif.service_type}")
        print(f"Дата работы: {notif.date_of_work}")
        print(f"Дата публикации: {notif.publishing_date}")
        print(f"Заголовок: {notif.work_header}")
        print(f"Ссылка: {notif.link}")
        print(f"Описание: {notif.description}")
        print('-------------------')