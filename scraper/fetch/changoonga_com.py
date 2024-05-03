from base.scraper import Scraper
from base.url_generator import URLGenerator
from base.types import BeautSoupType
from base.types import ScraperArticleType
from base.utils import nodes_to_lines
from base.utils import join_lines
from base.utils import iso_date_to_utc
from base.utils import normalize_iso_date
from base.utils import json_search_from_tag

def gen_xml_urls(scraper: Scraper, generator: URLGenerator) -> list[str]:
  return (generator
    .template('{base_url}/{path}')
    .static_params({'base_url': scraper.base_url})
    .each(name='path', values=[
      'feed/',
      'category/hardnews/feed/',
      'category/morelia/feed/',
      'category/michoacan/feed/'
    ])
    .generate()
  )

def parse_xml_urls(scraper: Scraper, soup: BeautSoupType) -> list[str]:
  return [link.text for link in soup.select('rss channel item link')]

def parse_article(scraper: Scraper, soup: BeautSoupType, article: ScraperArticleType) -> ScraperArticleType:
  jsonSearch = json_search_from_tag(soup, 'script#tie-schema-json[type="application/ld+json"]')

  # author
  article.author = jsonSearch.search('author.name')

  # date - to UTC from format: 2024-04-30T16:54:08-05:00
  date_str = jsonSearch.search('datePublished')
  article.published_time = iso_date_to_utc(date_str)

  # content - remove first paragraph
  node_set = soup.select('.entry-content > p:nth-of-type(n+2)')
  node_set = nodes_to_lines(node_set)
  article.content = join_lines(node_set)

  return article

def get_scraper() -> Scraper:
  return (
    Scraper('https://www.changoonga.com')
    .generate_xml_urls(gen_xml_urls)
    .parse_xml_urls(parse_xml_urls)
    .parse_article_content(parse_article)
    .write_articles_to_db()
    # .debug()
  )

if __name__ == "__main__":
  get_scraper().run()
