import time

def my_task():
    # Your task logic here
    pass

interval = 10  # Interval in seconds

while True:
    try:
        my_task()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        time.sleep(interval)