from base.scraper import Scraper
from base.url_generator import URLGenerator
from base.types import BeautSoupType
from base.types import ScraperArticleType
from base.utils import nodes_to_lines
from base.utils import join_lines
from base.utils import json_search_from_tag
from base.utils import normalize_iso_date
from base.utils import iso_date_to_utc
from base.utils import filter_lines_starting_with

def gen_xml_urls(scraper: Scraper, generator: URLGenerator) -> list[str]:
  return (generator
    .template('{base_url}/{path}')
    .static_params({'base_url': scraper.base_url})
    .each(name='path', values=['rss.xml', 'local/rss.xml', 'policiaca/rss.xml', 'cultura/rss.xml'])
    .generate()
  )

def parse_xml_urls(scraper: Scraper, soup: BeautSoupType) -> list[str]:
  links = soup.select('rss channel item link')
  return [link.text for link in links]

def parse_article(scraper: Scraper, soup: BeautSoupType, article: ScraperArticleType) -> ScraperArticleType:
  json = json_search_from_tag(soup)

  # author
  author_str = json.search('author.name').split('/')[0].strip()
  article.author = author_str

  # date
  date_str = json.search('datePublished')
  date_str = normalize_iso_date(date_str[:-3], '%Y-%m-%dT%H:%M:%S', 5)
  article.published_time = iso_date_to_utc(date_str)

  # content
  node_set = soup.css.select('.content-body > div > p')
  node_set = [p for p in node_set if not p.select_one('article, a, .picture')]
  node_set = nodes_to_lines(node_set)
  start_removals = ['Te puede interesar', 'También lee:', 'Lee también:', 'Suscríbete a nuestro Newsletter']
  node_set = filter_lines_starting_with(node_set, start_removals)
  article.content = join_lines(node_set)

  return article

def get_scraper() -> Scraper:
  return (
    Scraper('https://www.elsoldemorelia.com.mx', refresh_interval_sec=10)
    .generate_xml_urls(gen_xml_urls)
    .parse_xml_urls(parse_xml_urls)
    .parse_article_content(parse_article)
    .write_articles_to_db()
  )

if __name__ == "__main__":
  get_scraper().run()