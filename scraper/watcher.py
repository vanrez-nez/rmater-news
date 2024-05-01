import subprocess
import time
import logging
import atexit
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

observer = None

def run():
    command = ["poetry run python index.py", "Change detected"]
    subprocess.run(command, shell=True)

class CustomEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        ignore = ["__pycache__", "cache", "storage", "queue.lock", "."]
        if any(x in event.src_path for x in ignore): return
        logging.info(f"{event.event_type} - {event.src_path}")
        run()

def start_observer():
    global observer
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = CustomEventHandler()
    observer = Observer()
    observer.schedule(event_handler, '.', recursive=True)
    observer.start()
    logging.info("Watching for changes...")
    try:
        while True:
            time.sleep(1)
            print("Running...")
    except:
        stop_observer()

def stop_observer():
    global observer
    logging.info("Exiting from watcher...")
    if observer is not None:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    atexit.register(stop_observer)
    start_observer()
    run()