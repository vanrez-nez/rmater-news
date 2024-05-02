from base.scraper import Scraper
from base.url_generator import URLGenerator
from base.types import BeautSoupType
from base.types import ScraperArticleType
from base.utils import nodes_to_lines
from base.utils import join_lines
from base.utils import json_search_from_tag
from base.utils import iso_date_to_utc

def gen_page_urls(scraper: Scraper, generator: URLGenerator) -> list[str]:
  return (generator
    .template('{base_url}/seccion/{section}/page/{page_num}')
    .static_params({'base_url': scraper.base_url})
    .each(name='section', values=['michoacan', 'seguridad', 'seguridad/accidente'])
    .each(name='page_num', values=range(1, 5))
    .generate()
  )

def parse_page_urls(scraper: Scraper, soup: BeautSoupType) -> list[str]:
  return [a.attrs['href'] for a in soup.select('h2.post-box-title a')]

def parse_article(scraper: Scraper, soup: BeautSoupType, article: ScraperArticleType) -> ScraperArticleType:
  jsonSearch = json_search_from_tag(soup)

  # author
  article.author = jsonSearch.search('"@graph"[?"@type"==[\'Person\']].name | [0]')

  # date
  date_str = jsonSearch.search('"@graph"[*].datePublished | [0]')
  article.published_time = iso_date_to_utc(date_str)

  # content
  node_set = soup.select('.entry p')
  node_set = nodes_to_lines(node_set)
  article.content = join_lines(node_set)

  return article

def get_scraper() -> Scraper:
  return (
    Scraper('https://www.lavozdemichoacan.com.mx')
    .generate_page_urls(gen_page_urls)
    .parse_page_urls(parse_page_urls)
    .parse_article_content(parse_article)
    .write_articles_to_db()
    # .debug()
  )

if __name__ == "__main__":
  get_scraper().run()
