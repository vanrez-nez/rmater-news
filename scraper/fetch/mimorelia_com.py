from base.scraper import Scraper
from base.url_generator import URLGenerator
from base.types import BeautSoupType
from base.types import ScraperArticleType
from base.types import JSONSearchType
from base.utils import nodes_to_lines
from base.utils import join_lines
from base.utils import iso_date_to_utc
from base.utils import filter_lines_starting_with

def gen_json_urls(scraper: Scraper, generator: URLGenerator) -> list[str]:
  return (generator
    .template('{base_url}/api/v1/collections/{collection}?offset={offset}&limit=25')
    .static_params({'base_url': scraper.base_url})
    .each(name='collection', values=[
      'morelia-noticias',
      'michoacan-noticias',
      'politica-noticias',
      'economia-noticias',
      'deportes-noticias',
      'cultura-noticias',
      'nota-roja-noticias',
      'eventos'
    ])
    .each(name='offset', values=[0, 25, 50])
    .generate()
  )

def parse_json_urls(scraper: Scraper, json_search: JSONSearchType) -> list[str]:
  return json_search.search('items[*].story.url')

def parse_article(scraper: Scraper, soup: BeautSoupType, article: ScraperArticleType) -> ScraperArticleType:\
  # author
  article.author = soup.select_one('meta[name="author"]').attrs['content']

  # date
  date_str = soup.select_one('time').attrs['datetime']
  article.published_time = iso_date_to_utc(date_str)

  # content
  node_set = soup.select('.arr--text-element')
  start_removals = ['Síguenos en Google News']
  node_set = nodes_to_lines(node_set)
  node_set = filter_lines_starting_with(node_set, start_removals)
  article.content = join_lines(node_set)

  return article

def get_scraper() -> Scraper:
  return (
    Scraper('https://mimorelia.com')
    .generate_json_urls(gen_json_urls)
    .parse_json_urls(parse_json_urls)
    .parse_article_content(parse_article)
    .write_articles_to_db()
    # .debug()
  )

if __name__ == "__main__":
  get_scraper().run()
