import emoji
from pytz import timezone
from bs4 import BeautifulSoup
from .cached_request import get_url
from .scraper_utils import write_articles, parse_date, parse_time, convert_to_utc

BASE_URL = 'https://www.quadratin.com.mx'

def get_rss_links():
  url = f'{BASE_URL}/rss'
  response = get_url(url, extension='xml')
  soup = BeautifulSoup(response, 'lxml-xml')
  links = soup.select('channel item link')
  # extract link.text from each element of links
  return [link.text for link in links]

def get_page_links(url):
  response = get_url(url, extension='html')
  soup = BeautifulSoup(response, 'html.parser')
  links = soup.select('.q-notice a:not(.tag-container)')
  # extract link['href'] from each element of links
  return [link['href'] for link in links]

def merge_date_time(date, time):
  return date.replace(hour=time.hour, minute=time.minute)

def get_article(url):
  response = get_url(url, cache_duration=3600*24*30, extension='html')
  soup = BeautifulSoup(response, 'html.parser')
  title = soup.select_one('h1').text.strip()
  content = soup.select_one('.q-content__info')
  # remove emojis and strip the text
  content = [p.get_text(strip=True, separator=' ') for p in content]
  content = [emoji.replace_emoji(p, ' ') for p in content]
  content = ' '.join(content)

  author = soup.select_one('.q-content__redacted').text.strip()
  date_str = soup.select_one('.q-content__time .date').text
  time_str = soup.select_one('.q-content__time .hour').text
  date = merge_date_time(parse_date(date_str), parse_time(time_str))
  tz = timezone('America/Mexico_City')
  date = tz.localize(date)
  date = convert_to_utc(date.isoformat())
  return {
    'title': title,
    'content': content,
    'author': author,
    'src': url,
    'date': date,
  }

def get_section_links(section_name, max_pages):
  links = []

  for i in range(1, max_pages + 1):
    url = f'{BASE_URL}/{section_name}'
    if i > 1:
      url += f'/page/{i}/'
    links.extend(get_page_links(url))
  return links

def fetch():
  links = get_rss_links()
  sections = [
    'principal',
    'politica',
    'sucesos',
    'justicia',
    'Deportes',
    'municipios',
    'entretenimiento',
    'educativas'
  ]
  for section in sections:
    links.extend(get_section_links(section, 2))
  # remove duplicates
  links = list(set(links))
  articles = [get_article(link) for link in links]
  write_articles(BASE_URL, articles)

if __name__ == "__main__":
  fetch()