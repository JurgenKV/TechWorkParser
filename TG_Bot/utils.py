# import pyshorteners

import LOG

def shorten_url(url):
    # import pyshorteners.shorteners

    try:
        #shortener = pyshorteners.Shortener()
        #short_url = shortener.tinyurl.short(url)
        #return short_url
        return url
    except Exception as e:
        LOG.error(f"Ошибка при сокращении ссылки: {e}")
        return url
