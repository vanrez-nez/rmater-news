import asyncio
from typing import List
from base.scraper_queue import ScraperQueue
from base.cache_pruner import prune_cache_files
from transform.geo_tagging import run as transform_run
import fetch.elsoldemorelia_com_mx
import fetch.mimorelia_com
import fetch.cbtelevision_com_mx
import fetch.changoonga_com
import fetch.lavozdemichoacan_com_mx
import fetch.primeraplana_mx
import fetch.quadratin_com_mx

# https://pcmnoticias.mx/category/noticias/michoacan/
# https://cambiodemichoacan.com.mx/category/morelia/
# https://1plana.com/ultima_hora/estatales/
# https://gentedelbalsas.mx/category/estatales/
# https://sistemamichoacano.tv/category/noticas/michoacan/

async def start() -> None:
    # print("OPENAI_API_KEY:", os.environ.get("OPENAI_API_KEY"))
    # prune_cache_files()
    await ScraperQueue().add([
        fetch.elsoldemorelia_com_mx.get_scraper(),
        fetch.mimorelia_com.get_scraper(),
        fetch.cbtelevision_com_mx.get_scraper(),
        fetch.changoonga_com.get_scraper(),
        fetch.lavozdemichoacan_com_mx.get_scraper(),
        fetch.primeraplana_mx.get_scraper(),
        fetch.quadratin_com_mx.get_scraper(),
    ]).start()
    # transform_run()


if __name__ == "__main__":
    asyncio.run(start())
