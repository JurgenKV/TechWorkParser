import re
from datetime import datetime

import locale
import LOG

class UniversalDate:
    def __init__(self, date_string):
        self.date_string = date_string
        self.date_object = datetime(year=1, month=1, day=1)
    def parse_date_auto(self):
        # Список возможных форматов даты
        #locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        locale.setlocale(locale.LC_TIME, 'Russian_Russia.1251')
        date_formats = [
            "%d %B %Y",  # Пример: "10 May 2025"
            "%d.%m.%Y",  # Пример: "10.05.2025"
            "%Y-%m-%d",  # Пример: "2025-05-10"
            "%d/%m/%Y",  # Пример: "10/05/2025"
            "%B %d, %Y",  # Пример: "May 10, 2025"
        ]

        for fmt in date_formats:
            try:
                # Пытаемся преобразовать строку в объект datetime
                self.data_object = datetime.strptime(self.date_string, fmt)
            except ValueError:
                continue

        # Если ни один формат не подошел, вызываем ошибку
        LOG.error(f"Невозможно распознать дату: {self.date_string}")
        raise ValueError(f"Невозможно распознать дату: {self.date_string}")


    def parse_date_hard(self):
        # Словарь для замены русских названий месяцев
        month_mapping = {
            "янв": "01", "фев": "02", "мар": "03", "апр": "04",
            "май": "05", "июн": "06", "июл": "07", "авг": "08",
            "сен": "09", "окт": "10", "ноя": "11", "дек": "12", "мая": "05"
        }

        # Разбиваем строку на части
        parts = self.date_string.split()
        if len(parts) != 3:
            LOG.error(f"Неверный формат даты: {self.date_string}")
            raise ValueError(f"Неверный формат даты: {self.date_string}")

        day, month_name, year = parts
        month = month_mapping.get(month_name[:3].lower())  # Берем первые 3 буквы месяца
        if not month:
            LOG.error(f"Неизвестный месяц: {month_name}")
            raise ValueError(f"Неизвестный месяц: {month_name}")

        # Формируем новую строку в формате, который понимает datetime
        formatted_date = f"{day}.{month}.{year}"
        try:
            self.date_object = datetime.strptime(formatted_date, "%d.%m.%Y")
        except ValueError as e:
            LOG.error(f"Невозможно распознать дату: {self.date_string}")
            raise ValueError(f"Невозможно распознать дату: {self.date_string}") from e

    def to_format(self, output_format="%d.%m.%Y"):
        # Преобразуем дату в указанный формат
        return self.date_object.strftime(output_format)

    @staticmethod
    def parse_date_from_text(text):
        dates = re.findall(r'\d{2}\.\d{2}\.\d{4}', str(text))
        if not dates:
            list.append(dates, UniversalDate.parse_date_with_month_word(text) )
        if dates:
            return dates[0]
        else:
            return "00.00.0000"

    @staticmethod
    def parse_date_with_month_word(text):
        date = re.findall(r'\b\d{1,2} (?:января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря) \d{4}\b', str(text))
        if date:
            UD = UniversalDate(str(date[0]).strip())
            UD.parse_date_hard()
            return UD.to_format()
