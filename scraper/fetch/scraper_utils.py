# from dateutil import parser
from datetime import datetime
import re
import locale
from db_handler import DbHandler

def clean_date_str(date_str):
    regex = r'\b\d{1,2} de [a-zA-Z]+ de \d{4}\b'
    match = re.search(regex, date_str)
    if match:
        date_str = match.group(0)
    return date_str

def parse_date(date_str, locale_str = 'es_ES'):
    # Set the locale
    locale.setlocale(locale.LC_TIME, locale_str)

    # clear spaces and new lines
    date_str = date_str.replace('\n', '').strip()

    # parse the date string
    parsed_date = datetime.strptime(date_str, '%d de %B de %Y')

    # Reset the locale to default
    locale.setlocale(locale.LC_TIME, '')
    return parsed_date

def parse_time(time_str):
    # clear spaces and new lines
    time_str = time_str.replace('\n', '').strip()

    # parse the time string
    parsed_time = datetime.strptime(time_str, '%H:%M')

    return parsed_time

def write_articles(url, articles):
    db_handler = DbHandler()
    for article in articles:
        # hash the url to get a unique id positive int
        db_handler.save_entry(
        url,
        article['title'],
        article['content'],
        article['author'],
        article['src'],
        article['date']
        )