import time
import os
# import run from the transform module
from fetch.quadratin_com_mx import fetch as quadratin_fetch
from fetch.mimorelia_com import fetch as mimorelia_fetch
from fetch.elsoldemorelia_com_mx import fetch as elsoldemorelia_fetch
from fetch.changoonga_com import fetch as changoonga_fetch

def fetch_all():
    # print environment variables
    print("OPENAI_API_KEY:", os.environ.get("OPENAI_API_KEY"))
    quadratin_fetch()
    mimorelia_fetch()
    elsoldemorelia_fetch()
    changoonga_fetch()
    print("Done fetching")

if __name__ == "__main__":
    fetch_all()