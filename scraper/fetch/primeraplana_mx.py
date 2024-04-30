import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from .cached_request import get_url
from .scraper_utils import write_articles, convert_to_utc

BASE_URL = 'https://primeraplana.mx'

def get_links(section, page_num):
  url = f'{BASE_URL}/archivos/category/{section}/page/{page_num}/rss'
  response = get_url(url, extension='xml')
  soup = BeautifulSoup(response, 'lxml-xml')
  links = soup.select('rss channel item link')
  # extract link.text from each element of links
  return [link.text for link in links]

def get_article(url):
  response = get_url(url, cache_duration=3600*24*30, extension='html')
  soup = BeautifulSoup(response, 'html.parser')
  title = soup.select_one('h1').text
  content = soup.select('.td-post-content p')
  content = [p.get_text(strip=True, separator=' ') for p in content]
  content = ' '.join(content)
  author = soup.select_one('.td-post-author-name a').text
  date = soup.select_one('meta[property="article:published_time"]').attrs['content']
  date = convert_to_utc(date)
  return {
    'title': title,
    'content': content,
    'author': author,
    'src': url,
    'date': date,
  }

def fetch():
  links = []
  sections = [
    'michoacan',
    'morelia'
  ]
  for section in sections:
    for page in range(1, 5):
      links.extend(get_links(section, page))
  links = list(set(links))
  articles = [get_article(link) for link in links]
  write_articles(BASE_URL, articles)

if __name__ == "__main__":
  fetch()
