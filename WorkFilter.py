from datetime import datetime, timedelta

from TechData import TechData


def get_publication_date_datetime(str_date):
    try:
        if str_date is not None or str_date != "":
            date = datetime.strptime(str_date, "%d.%m.%Y")
        else:
            return datetime.now().today()
    except Exception as v:
        print(v)
        print(str_date)
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
