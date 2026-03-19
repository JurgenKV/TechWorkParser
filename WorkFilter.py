from datetime import datetime, timedelta

from TechData import TechData
import LOG

def get_publication_date_datetime(str_date):
    try:
        if str_date is not None or str_date != "" or str_date != "None":
            date = datetime.strptime(str_date, "%d.%m.%Y")
        else:
            return datetime.now().today()
    except Exception as v:
        print(v)
        print(str_date)
        LOG.warning(str(v) + str_date)
        return datetime.now().today()
    return date


def get_works_by_period(works: list[TechData], days):
    current_date = datetime.now()

    start_date = current_date - timedelta(days=days)

    filtered_works = [
        work for work in works
        if start_date <= get_publication_date_datetime(work.publishing_date) <= current_date
    ]

    return filtered_works

def sort_by_nearest_work(works: list[TechData]):
    return sorted(works, key=lambda x: get_publication_date_datetime(x.publishing_date), reverse=True)

def fill_empty_work_fields_by_const_text(works: list[TechData]):
    for work in works:
        if work.date_of_work is None or work.date_of_work == "" or work.date_of_work == " " or work.date_of_work == "None":
            work.const_text = "На сайте"
        if work.publishing_date is None or work.publishing_date == "" or work.publishing_date == " " or work.publishing_date == "None":
            work.const_text = "На сайте"
        if work.description is None or work.description == "" or work.description == " " or work.description == "None":
            work.const_text = "На сайте"
    return works