from base.scraper import Scraper
from base.url_generator import URLGenerator
from base.types import BeautSoupType
from base.types import ScraperArticleType
from base.utils import nodes_to_lines
from base.utils import join_lines
from base.utils import iso_date_to_utc

def gen_xml_urls(scraper: Scraper, generator: URLGenerator) -> list[str]:
  return (generator
    .template('{base_url}/rss')
    .static_params({'base_url': scraper.base_url})
    .generate()
  )

def gen_page_urls(scraper: Scraper, generator: URLGenerator) -> list[str]:
  return (generator
    .template('{base_url}/{section}{page}')
    .static_params({'base_url': scraper.base_url})
    .each(name='section', values=[
      'politica',
      'sucesos',
      'justicia',
      'Deportes',
      'municipios',
      'entretenimiento',
      'educativas'
    ])
    .each(name='page', values=[f'/page/{i}' for i in range(1, 4)])
    .generate()
  )

def parse_page_urls(scraper: Scraper, soup: BeautSoupType) -> list[str]:
  links = soup.select('.q-notice a:not(.tag-container)')
  return [link['href'] for link in links]

def parse_xml_urls(scraper: Scraper, soup: BeautSoupType) -> list[str]:
  links = soup.select('rss channel item link')
  return [link.text for link in links]

def parse_article(scraper: Scraper, soup: BeautSoupType, article: ScraperArticleType) -> ScraperArticleType:
  # author
  author = soup.select_one('.q-content__redacted').text.strip()
  author = author.split('/')[0]
  article.author = author

  # date with format 2024-05-01T12:38:20-06:00
  date_str = soup.select_one('meta[property="article:published_time"]').attrs['content']
  article.published_time = iso_date_to_utc(date_str)

  # content
  node_set = soup.select_one('.q-content__info')
  node_set = nodes_to_lines(node_set)
  article.content = join_lines(node_set)

  return article

def get_scraper() -> Scraper:
  return (
    Scraper('https://www.quadratin.com.mx')
    .generate_xml_urls(gen_xml_urls)
    .generate_page_urls(gen_page_urls)
    .parse_xml_urls(parse_xml_urls)
    .parse_page_urls(parse_page_urls)
    .parse_article_content(parse_article)
    .write_articles_to_db()
    # .debug()
  )

if __name__ == "__main__":
  get_scraper().run()