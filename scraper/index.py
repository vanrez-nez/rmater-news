from typing import List
from base.scraper_queue import ScraperQueue
import fetch.elsoldemorelia_com_mx
import fetch.mimorelia_com

# https://pcmnoticias.mx/category/noticias/michoacan/
# https://cambiodemichoacan.com.mx/category/morelia/
# https://1plana.com/ultima_hora/estatales/
# https://gentedelbalsas.mx/category/estatales/
# https://sistemamichoacano.tv/category/noticas/michoacan/

def start() -> None:
    # print("OPENAI_API_KEY:", os.environ.get("OPENAI_API_KEY"))
    ScraperQueue().add([
        # fetch.elsoldemorelia_com_mx.get_scraper()
        fetch.mimorelia_com.get_scraper()
    ]).start()


if __name__ == "__main__":
    start()
