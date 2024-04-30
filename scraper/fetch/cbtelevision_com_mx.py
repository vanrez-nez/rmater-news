import re
from datetime import datetime, timedelta
from .cached_request import get_url
from .scraper_utils import write_articles, parse_date, clean_date_str, convert_to_utc
from bs4 import BeautifulSoup

BASE_URL = 'https://cbtelevision.com.mx'

def get_rss_links(section):
  url = f'{BASE_URL}/noticias/{section}/feed/'
  response = get_url(url, extension='xml')
  soup = BeautifulSoup(response, 'lxml-xml')
  links = soup.select('rss channel item link')
  # extract link.text from each element of links
  return [link.text for link in links]

def get_article(url):
  response = get_url(url, cache_duration=3600*24*30, extension='html', cache=False)
  soup = BeautifulSoup(response, 'html.parser')
  title = soup.select_one('h1').getText(strip=True)
  content = soup.select('.td-post-content p')
  content = [p.get_text(strip=True, separator=' ') for p in content]
  content = ' '.join(content)
  author = soup.select_one('.tdb-author-name').text.strip()
  json_content = soup.select_one('.yoast-schema-graph[type="application/ld+json"]').get_text(strip=True)
  try:
    matches = re.search(r'(?<=datePublished":").*?(?=")', json_content)
    date_str = matches.group(0)
    date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
    date = convert_to_utc(date.isoformat())
  except:
    date_str = soup.select_one('meta[property="article:published_time"]').attrs('content')
    date = convert_to_utc(date_str)
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
    'nota-roja',
    'morelia',
    'michoacan',
  ]
  for section in sections:
    links.extend(get_rss_links(section))
  links = list(set(links))
  articles = [get_article(link) for link in links]
  write_articles(BASE_URL, articles)

if __name__ == "__main__":
  fetch()