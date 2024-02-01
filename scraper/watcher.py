import subprocess
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CustomEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        logging.info(f"{event.event_type} - {event.src_path}")
        command = ["poetry run python index.py", "Change detected"]
        subprocess.run(command, shell=True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = CustomEventHandler()
    observer = Observer()
    observer.schedule(event_handler, '.', recursive=True)
    observer.start()
    print("Watcher started")
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()