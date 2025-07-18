import Parsers
from TechData import TechData

if __name__ == '__main__':
    all_tech_list = list()
    #all_tech_list.extend(Parsers.parse_erip('ERIP')) # NEED UPD
    #all_tech_list.extend(Parsers.parse_BFT('BFT')) # NEED UPD
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
    #all_tech_list.extend(Parsers.parse_Kupala('Kupala'))
    #all_tech_list.extend(Parsers.parse_BVFB('BVFB'))
    #all_tech_list.extend(Parsers.parse_NBRB('NBRB'))
    #all_tech_list.extend(Parsers.parse_Bank_AlfaRu('Bank_AlfaRu'))
    #all_tech_list.extend(Parsers.parse_Bank_Belarusbank('Bank_Belarusbank'))
    #all_tech_list.extend(Parsers.parse_Bank_BSB('Bank_BSB'))
    #all_tech_list.extend(Parsers.parse_Bank_BTA('Bank_BTA'))
    #all_tech_list.extend(Parsers.parse_Bank_BankReshenii('Bank_BankReshenii'))
    #all_tech_list.extend(Parsers.parse_Bank_BELWEB('Bank_BELWEB'))
    #all_tech_list.extend(Parsers.parse_Bank_BelAgro('Bank_BelAgro')) # need some fix
    #all_tech_list.extend(Parsers.parse_Bank_Belinvest('Bank_Belinvest')) # need selenium timeout >20
    #all_tech_list.extend(Parsers.parse_Bank_MTB('Bank_MTB'))
    #all_tech_list.extend(Parsers.parse_Bank_Paritet('Bank_Paritet'))
    #all_tech_list.extend(Parsers.parse_Bank_Zepter('Bank_Zepter'))
    #all_tech_list.extend(Parsers.parse_Bank_Sberbank('Bank_Sberbank')) # problem with year after NY
    #all_tech_list.extend(Parsers.parse_Bank_Priorbank('Bank_Priorbank'))

    for notif in all_tech_list:
        print(f"Сервис: {notif.service_type}")
        print(f"Дата работы: {notif.date_of_work}")
        print(f"Дата публикации: {notif.publishing_date}")
        print(f"Заголовок: {notif.work_header}")
        print(f"Ссылка: {notif.link}")
        print(f"Описание: {notif.description}")
        print('-------------------')