from datetime import datetime

import Parsers
from TechData import TechData

if __name__ == '__main__':
    timeStart = datetime.now().time().second
    all_tech_list = list()
    #all_tech_list.extend(Parsers.parse_ERIP('ЕРИП'))
    # all_tech_list.extend(Parsers.parse_BFT('БФТ'))
    all_tech_list.extend(Parsers.parse_BPC('БПЦ'))
    # all_tech_list.extend(Parsers.parse_MNS('МНС'))
    # all_tech_list.extend(Parsers.parse_OAIS('ОАИС'))
    # all_tech_list.extend(Parsers.parse_A1('A1')) # cringo
    # all_tech_list.extend(Parsers.parse_MTS('МТС')) # cringo
    # all_tech_list.extend(Parsers.parse_Life('Life'))
    # all_tech_list.extend(Parsers.parse_Seventech('Seventech'))
    # all_tech_list.extend(Parsers.parse_Beltelecom('Beltelecom')) # cringo
    # all_tech_list.extend(Parsers.parse_Delova9Seti('Деловая Сеть'))
    # all_tech_list.extend(Parsers.parse_Hoster('Hoster'))
    # all_tech_list.extend(Parsers.parse_BeCloud('BeCloud'))
    # all_tech_list.extend(Parsers.parse_Oplati('Оплати'))
    # all_tech_list.extend(Parsers.parse_Kupala('Kupala'))
    # all_tech_list.extend(Parsers.parse_BVFB('БВФБ'))
    # all_tech_list.extend(Parsers.parse_NBRB('НБРБ'))
    # all_tech_list.extend(Parsers.parse_Bank_AlfaRu('Альфа-Банк Россия'))
    # all_tech_list.extend(Parsers.parse_Bank_Belarusbank('Белурусьбанк'))
    # all_tech_list.extend(Parsers.parse_Bank_BSB('БСБ Банк'))
    # all_tech_list.extend(Parsers.parse_Bank_BTA('БТА Банк'))
    # all_tech_list.extend(Parsers.parse_Bank_BankReshenii('Банк Решений'))
    # all_tech_list.extend(Parsers.parse_Bank_BELWEB('БЕЛВЕБ Банк'))
    # all_tech_list.extend(Parsers.parse_Bank_BelAgro('Белагропромбанк')) # need some fix
    # all_tech_list.extend(Parsers.parse_Bank_Belinvest('Белинвестбанк')) # need selenium timeout >20
    # all_tech_list.extend(Parsers.parse_Bank_MTB('МТБ Банк'))
    # all_tech_list.extend(Parsers.parse_Bank_Paritet('Паритетбанк'))
    # all_tech_list.extend(Parsers.parse_Bank_Zepter('Цептер Банк'))
    # all_tech_list.extend(Parsers.parse_Bank_Sberbank('Сбербанк')) # problem with year after NY
    # all_tech_list.extend(Parsers.parse_Bank_Priorbank('Приорбанк'))
    timeEnd = datetime.now().time().second

    print(timeEnd - timeStart)
    for notif in all_tech_list:
        print(f"Сервис: {notif.service_type}")
        print(f"Дата работы: {notif.date_of_work}")
        print(f"Дата публикации: {notif.publishing_date}")
        print(f"Заголовок: {notif.work_header}")
        print(f"Ссылка: {notif.link}")
        print(f"Описание: {notif.description}")
        print('-------------------')