import time
import os
# import run from the transform module
from fetch.quadratin_com_mx import fetch as quadratin_fetch
from fetch.mimorelia_com import fetch as mimorelia_fetch
from fetch.elsoldemorelia_com_mx import fetch as elsoldemorelia_fetch
from fetch.changoonga_com import fetch as changoonga_fetch

def fetch_all():
    # print environment variables
    # print("OPENAI_API_KEY:", os.environ.get("OPENAI_API_KEY"))
    print("Fetching...")
    quadratin_fetch()
    mimorelia_fetch()
    elsoldemorelia_fetch()
    changoonga_fetch()
    print("Done fetching")


def run():
    # interval = int(os.environ.get("SCRAPPER_UPDATE_INTERVAL", 60))
    fetch_all()
    # time.sleep(interval)

if __name__ == "__main__":
    run()