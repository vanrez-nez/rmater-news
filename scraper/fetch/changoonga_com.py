import json
from cached_request import get_url
from scraper_utils import write_articles, parse_date, clean_date_str
from bs4 import BeautifulSoup

BASE_URL = 'https://www.changoonga.com'


def get_rss_links(section):
  url = f'{BASE_URL}/category/{section}/feed/'
  if section == 'index':
    url = f'{BASE_URL}/feed/'
  response = get_url(url, extension='xml')
  soup = BeautifulSoup(response, 'lxml-xml')
  links = soup.select('rss channel item link')
  # extract link.text from each element of links
  return [link.text for link in links]

def get_article(url):
  response = get_url(url, cache_duration=3600*24*30, extension='html')
  soup = BeautifulSoup(response, 'html.parser')
  title = soup.select_one('h1').text
  content = soup.select('.entry-content p:not(:first-child)')
  content = [p.get_text(strip=True) for p in content]
  author = content.pop(0)
  content = '\n'.join(content)
  date_str = soup.select_one('.date').get_text(strip=True)
  date_str = clean_date_str(date_str)
  date = parse_date(date_str)
  return {
    'title': title,
    'content': content,
    'author': author,
    'src': url,
    'date': date.isoformat(),
  }

def write_json(data):
  with open('./outputs/changoonga.com.json', 'w') as file:
    json.dump(data, file, indent=2)

if __name__ == "__main__":
  links = []
  sections = [
    'index',
    'hardnews',
    'morelia',
    'michoacan',
  ]
  for section in sections:
    links.extend(get_rss_links(section))
  links = list(set(links))
  articles = [get_article(link) for link in links]
  write_articles(BASE_URL, articles)