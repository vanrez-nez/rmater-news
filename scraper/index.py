import time
import os

def my_task():
    # print environment variables
    print("OPENAI_API_KEY:", os.environ.get("OPENAI_API_KEY"))

if __name__ == "__main__":
    my_task()