import json
import jmespath
from bs4 import BeautifulSoup
from .cached_request import get_url
from .scraper_utils import write_articles

BASE_URL = 'https://mimorelia.com'

def get_links(collection, page_num):
  url = f'{BASE_URL}/api/v1/collections/{collection}?offset={page_num}&limit=25'
  response = get_url(url, extension='json')
  data = json.loads(response)
  return jmespath.search('items[*].story.url', data)

def get_article(url):
  response = get_url(url, cache_duration=3600*24*30, extension='html')
  soup = BeautifulSoup(response, 'html.parser')
  title = soup.select_one('h1').text
  content_els = soup.select('.arr--text-element')
  # filter out el if el.text starts with Síguenos en Google News
  content_els = [el for el in content_els if not el.text.startswith('Síguenos en Google News')]
  content = [el.text for el in content_els]
  content = '\n'.join(content)
  author = soup.select_one('.arr--caption-attribution').text
  date_str = soup.select_one('time').attrs['datetime']
  return {
    'title': title,
    'content': content,
    'author': author,
    'src': url,
    'date': date_str,
  }

def fetch():
  links = []
  sections = [
    'morelia-noticias',
    'michoacan-noticias',
    'politica-noticias',
    'economia-noticias',
    'deportes-noticias',
    'cultura-noticias',
    'nota-roja-noticias',
    'eventos'
  ]
  for section in sections:
    links.extend(get_links(section, 0))
  links = list(set(links))
  articles = [get_article(link) for link in links]
  write_articles(BASE_URL, articles)

if __name__ == "__main__":
  fetch()
