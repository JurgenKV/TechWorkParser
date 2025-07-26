import pyshorteners

import LOG

def shorten_url(url):
    try:
        shortener = pyshorteners.Shortener()
        short_url = shortener.tinyurl.short(url)
        return short_url
    except Exception as e:
        LOG.error(f"Ошибка при сокращении ссылки: {e}")
        return url
