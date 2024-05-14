import os
import json
from ollama import AsyncClient
from base.types import ScraperArticleType
from base.logger import log
from base.async_utils import async_wrapper
from database.db_handler import get_articles_without_location
from transform.prompts.geo_location import build_prompt

def get_articles() -> list[ScraperArticleType]:
  return get_articles_without_location(10)

async def query_ollama(article: ScraperArticleType) -> dict:
  host = os.environ.get("OLLAMA_HOST")
  client = AsyncClient(host=host)
  prompt = build_prompt(article.title, article.content)
  response = await client.chat(model='llama3', format='json', messages=[
    {
      'role': 'user',
      'content': prompt,
    },
  ])
  return response

async def run():
  articles = get_articles()
  for article in articles:
    response = await query_ollama(article)
    try:
      content = response.get('message', {}).get('content', {})
      json_response = json.loads(content)
      # validate response and required fields
      fields = ['pais', 'estado', 'ciudad', 'municipio', 'colonia', 'calle', 'numero', 'lugar']
      if not all(field in json_response for field in fields):
        log('Invalid response', json_response)
        continue
      log(f'{article.url}, Valid response {json_response}')
    except:
      log('Invalid JSON response', response)
      continue

    # log('Pais', json_response['pais'])
    # log('Estado', json_response['estado'])
    # log('Ciudad', json_response['ciudad'])
    # log('Municipio', json_response['municipio'])
    # log('Colonia', json_response['colonia'])
