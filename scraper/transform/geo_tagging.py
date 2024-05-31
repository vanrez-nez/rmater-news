import json
import os
from base.types import ScraperArticleType
from base.types import ArticleLocationType
from base.request import make_request
from base.logger import log
from base.logger import error
from base.logger import warn
from database.db_handler import get_articles_without_location
from database.db_handler import write_location
from base.article_location import ArticleLocation

def get_articles() -> list[ScraperArticleType]:
  return get_articles_without_location(100)

async def query_locations(article: ScraperArticleType) -> list[ArticleLocationType]:
  host = os.environ.get("RAG_LLM_HOST")
  # format url with params
  params = {
    'title': article.title,
    'content': article.content
  }
  url = f'{host}/geo_locate_article'
  response = await make_request(url, cache=False, form_data=params, method='POST')
  json_response = json.loads(response)
  return json_response

def parse_locations(locations: list[dict]) -> list[ArticleLocationType]:
  return [ArticleLocation(location) for location in locations]

def update_article_locations(article: ScraperArticleType, locations: list[ArticleLocationType]):
  if (len(locations) == 0):
    warn(f"No locations found for article: ({article.id}){article.url}")
    return
  log(f"Geo: ({article.id}): {article.url} with:")
  log(f"\t\t{', '.join([locations.name for locations in locations])}")
  for location in locations:
    write_location(article, location)

async def run():
  log("Running geo tagging transform")
  articles = get_articles()
  for article in articles:
    try:
      response = await query_locations(article)
      locations = parse_locations(response)
      update_article_locations(article, locations)
    except Exception as e:
      error(f"Error localizing article: {article.url}: {str(e)}")