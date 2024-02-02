import time
import os
# import run from the transform module
from transform.index import run
from fetch.quadratin_com_mx import fetch as quadratin_fetch

def my_task():
    # print environment variables
    print("OPENAI_API_KEY:", os.environ.get("OPENAI_API_KEY"))
    quadratin_fetch()

if __name__ == "__main__":
    my_task()