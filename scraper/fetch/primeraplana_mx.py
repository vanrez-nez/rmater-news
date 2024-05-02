from base.scraper import Scraper
from base.url_generator import URLGenerator
from base.types import BeautSoupType
from base.types import ScraperArticleType
from base.utils import nodes_to_lines
from base.utils import join_lines
from base.utils import iso_date_to_utc

def gen_xml_urls(scraper: Scraper, generator: URLGenerator) -> list[str]:
  return (generator
    .template('{base_url}/archivos/category/{section}/page/{page_num}/rss')
    .static_params({'base_url': scraper.base_url})
    .each(name='section', values=['michoacan', 'morelia'])
    .each(name='page_num', values=range(1, 5))
    .generate()
  )

def parse_xml_urls(scraper: Scraper, soup: BeautSoupType) -> list[str]:
  links = soup.select('rss channel item link')
  return [link.text for link in links]

def parse_article(scraper: Scraper, soup: BeautSoupType, article: ScraperArticleType) -> ScraperArticleType:

  # author
  article.author = soup.select_one('.td-post-author-name a').text

  # date
  date_str = soup.select_one('meta[property="article:published_time"]').attrs['content']
  article.published_time = iso_date_to_utc(date_str)

  # content
  node_set = soup.select('.td-post-content p')
  node_set = nodes_to_lines(node_set)
  article.content = join_lines(node_set)

  return article

def get_scraper() -> Scraper:
  return (
    Scraper('https://primeraplana.mx')
    .generate_xml_urls(gen_xml_urls)
    .parse_xml_urls(parse_xml_urls)
    .parse_article_content(parse_article)
    .write_articles_to_db()
    # .debug()
  )

if __name__ == "__main__":
  get_scraper().run()
