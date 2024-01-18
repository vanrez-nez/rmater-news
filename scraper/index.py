import time
import os

def my_task():
    # print environment variables
    print("OPENAI_API_KEY:", os.environ.get("OPENAI_API_KEY"))

interval = 1  # Interval in seconds

while True:
    try:
        my_task()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        time.sleep(interval)