import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from .cached_request import get_url
from .scraper_utils import write_articles, convert_to_utc

BASE_URL = 'https://www.lavozdemichoacan.com.mx'

def get_links(section, page_num):
  url = f'{BASE_URL}/seccion/{section}/page/{page_num}'
  response = get_url(url, extension='html')
  soup = BeautifulSoup(response, 'html.parser')
  links = soup.select('h2.post-box-title a')
  return [link['href'] for link in links]

def get_article(url):
  response = get_url(url, cache_duration=3600*24*30, extension='html')
  soup = BeautifulSoup(response, 'html.parser')
  title = soup.select_one('h1').text
  content = soup.select('.entry p')
  content = [p.get_text() for p in content]
  content = '\n'.join(content)
  author = 'La Voz de Michoacán'
  try:
    json_content = soup.select_one('body script[type="application/ld+json"]').get_text(strip=True)
    matches = re.search(r'(?<=datePublished":").*?(?=")', json_content)
    date_str = matches.group(0)
    date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
    date = convert_to_utc(date.isoformat())
  except:
    date = ''
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
    'seguridad/accidente'
  ]
  for section in sections:
    for page in range(1, 5):
      links.extend(get_links(section, page))
  links = list(set(links))

  articles = []
  for link in links:
    try:
      article = get_article(link)
      articles.append(article)
    except:
      print(f'Error while fetching: {link}')
      pass
  write_articles(BASE_URL, articles)

if __name__ == "__main__":
  fetch()
