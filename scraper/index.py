from typing import List
from base.url_generator import URLGenerator
from base.json_search import JSONSearch

import time
import os
# import run from the transform module
from fetch.quadratin_com_mx import fetch as quadratin_fetch
from fetch.mimorelia_com import fetch as mimorelia_fetch
from fetch.elsoldemorelia_com_mx import fetch as elsoldemorelia_fetch
from fetch.changoonga_com import fetch as changoonga_fetch
from fetch.lavozdemichoacan_com_mx import fetch as lavozdemichoacan_fetch
from fetch.cbtelevision_com_mx import fetch as cbtelevision_fetch
from fetch.primeraplana_mx import fetch as primeraplana_fetch
from base.url_generator import URLGenerator
from base.scraper import Scraper

def gen_json_urls(generator: URLGenerator) -> List[str]:
  return (generator
    .template('{base_url}/api/v1/collections/{section}?offset={offset}&limit=25')
    .static_params({'base_url': 'https://mimorelia.com'})
    .each(name='section', values=['morelia-noticias', 'economia-noticias', 'deportes-noticias', 'eventos'])
    .each(name='offset', values=range(0, 100, 25))
    .generate()
  )

def parse_json_urls(jsonSearch: JSONSearch) -> List[str]:
  return jsonSearch.search('items[*].story.url')

def fetch_all():
    # print environment variables
    # print("OPENAI_API_KEY:", os.environ.get("OPENAI_API_KEY"))
    print("Fetching...")
    # quadratin_fetch()
    # mimorelia_fetch()
    # elsoldemorelia_fetch()
    # changoonga_fetch()
    # lavozdemichoacan_fetch()
    # cbtelevision_fetch()
    # primeraplana_fetch()

    (Scraper
     .create('https://mimorelia.com')
     .generate_json_urls(gen_json_urls)
     .parse_json_urls(parse_json_urls)
     .run()
     .debug()
    )



    # urls = (URLGenerator
    #   .create()
    #   .template('{base_url}/api/v1/collections/{section}?offset={offset}&limit=25')
    #   .static_params({'base_url': 'https://mimorelia.com'})
    #   .each(name='section', values=['morelia-noticias', 'economia-noticias', 'deportes-noticias', 'eventos'])
    #   .each(name='offset', values=range(0, 10))
    #   .generate()
    # )
    # print(urls)


    # https://cambiodemichoacan.com.mx/category/morelia/
    # https://1plana.com/ultima_hora/estatales/
    # https://gentedelbalsas.mx/category/estatales/
    # https://sistemamichoacano.tv/category/noticas/michoacan/
    print("Done fetching")


def run():
    # interval = int(os.environ.get("SCRAPPER_UPDATE_INTERVAL", 60))
    fetch_all()
    # time.sleep(interval)


if __name__ == "__main__":
    run()
