from base.scraper import Scraper
from base.url_generator import URLGenerator
from base.types import BeautSoupType
from base.types import ScraperArticleType
from base.types import JSONSearchType
from base.utils import nodes_to_lines
from base.utils import join_lines
from base.utils import iso_date_to_utc
from base.utils import json_search_from_tag

def gen_xml_urls(scraper: Scraper, generator: URLGenerator) -> list[str]:
  return (generator
    .template('{base_url}/noticias/{section}/feed')
    .static_params({'base_url': scraper.base_url})
    .each(name='section', values=['nota-roja', 'morelia', 'michoacan'])
    .generate()
  )

def parse_xml_urls(scraper: Scraper, soup: BeautSoupType) -> list[str]:
  return [link.text for link in soup.select('rss channel item link')]

def parse_article(scraper: Scraper, soup: BeautSoupType, article: ScraperArticleType) -> ScraperArticleType:
  jsonSearch = json_search_from_tag(soup)

  # author
  article.author = jsonSearch.search('"@graph"[*].author.name | [0]')

  # date
  date_str = jsonSearch.search('"@graph"[*].datePublished | [0]')
  article.published_time = iso_date_to_utc(date_str)

  # content
  node_set = soup.select('.td-post-content p')
  node_set = nodes_to_lines(node_set)
  article.content = join_lines(node_set)

  return article

def get_scraper() -> Scraper:
  return (
    Scraper('https://cbtelevision.com.mx')
    .generate_xml_urls(gen_xml_urls)
    .parse_xml_urls(parse_xml_urls)
    .parse_article_content(parse_article)
    .write_articles_to_db()
    # .debug()
  )

if __name__ == "__main__":
  get_scraper().run()
