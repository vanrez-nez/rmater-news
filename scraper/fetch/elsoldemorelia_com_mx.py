import re
import emoji
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from .cached_request import get_url
from .scraper_utils import write_articles, convert_to_utc, parse_date, clean_date_str

BASE_URL = 'https://www.elsoldemorelia.com.mx'

def get_rss_links(section):
  url = f'{BASE_URL}/{section}/rss.xml'
  if section == 'index':
    url = f'{BASE_URL}/rss.xml'
  response = get_url(url, extension='xml')
  soup = BeautifulSoup(response, 'lxml-xml')
  links = soup.select('rss channel item link')
  # extract link.text from each element of links
  return [link.text for link in links]

def get_article(url):
  response = get_url(url, cache_duration=3600*24*30, extension='html')
  soup = BeautifulSoup(response, 'html.parser')

  title = soup.select_one('h1').getText(strip=True)
  content = soup.select('.content-body > div > p')
  # remove a paragraph if it contains an article tag
  content = [p for p in content if not p.select_one('article')]
  content = [p for p in content if not p.select_one('a')]
  # remove emojis and strip the text
  content = [p.get_text(strip=True, separator=' ') for p in content]
  content = [emoji.replace_emoji(p, ' ') for p in content]
  # remove tags that begin with any of the strings in the list to_remove
  to_remove = [
    'También te podría interesar:',
    'Lee también:',
    'También lee:'
    'Te puede interesar',
    '➡️ Suscríbete a nuestro Newsletter'
  ]
  content = [p for p in content if not any(p.startswith(s) for s in to_remove)]
  content = ' '.join(content)
  author = ''
  if soup.select_one('.byline'):
    author = soup.select_one('.byline').getText(strip=True)
  try:
    json_content = soup.select_one('script[type="application/ld+json"]').get_text(strip=True)
    matches = re.search(r'(?<=datePublished": ").*?(?=")', json_content)
    date_str = matches.group(0)
    date = datetime.strptime(date_str[:-3], '%Y-%m-%dT%H:%M:%S')
    date = date + timedelta(hours=5)
    date = convert_to_utc(date.isoformat())
  except:
    date_str = soup.select_one('.published-date').get_text(strip=True)
    date_str = clean_date_str(date_str)
    date = parse_date(date_str)
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
    'index',
    'local',
    'policiaca',
    'cultura'
  ]
  for section in sections:
    links.extend(get_rss_links(section))
  links = list(set(links))
  articles = [get_article(link) for link in links]
  write_articles(BASE_URL, articles)

if __name__ == "__main__":
  fetch()