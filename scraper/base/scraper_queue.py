import time
import os
from base.logger import log
from base.logger import error
from base.logger import warn
from typing import List
from base.types import ScraperType

class ScraperQueue:
  def __init__(self):
    self.id = id(self)
    self.queue: List[ScraperType] = []
    self.running: bool = False
    self.max_running_scrapers: int = 1
    log(f"New Queue ID: {self.id} - OS PID: {os.getpid()}")

  @property
  def running_count(self) -> int:
    return len([s for s in self.queue if s.running])

  def write_lock_file(self) -> None:
    with open('queue.lock', 'w') as f:
      f.write(str(self.id))

  def read_lock_file(self) -> str:
    with open('queue.lock', 'r') as f:
      return f.read()

  def is_lock_active(self) -> bool:
    lock_id = self.read_lock_file()
    return str(self.id) == lock_id

  def add(self, scraper: ScraperType|List[ScraperType]) -> 'ScraperQueue':
    scrapers = scraper if isinstance(scraper, list) else [scraper]
    for scraper in scrapers:
      # verify that scraper is not already in the queue by checking the base_url
      scraper_base_urls = [s.base_url for s in self.queue]
      if scraper.base_url not in scraper_base_urls:
        self.queue.append(scraper)
    return self

  def spawn(self) -> 'ScraperQueue':
    if self.running_count >= self.max_running_scrapers:
      return self
    for scraper in self.queue:
      dt = scraper.time_since_last_run()
      if not scraper.running and dt > scraper.refresh_interval_sec:
        try:
          scraper.run()
        except Exception as e:
          error(f"Error running scraper: {scraper.base_url}", e)
    return self

  def start(self) -> 'ScraperQueue':
    self.write_lock_file()
    if not self.running:
      self.running = True
      while self.running:
        if not self.is_lock_active():
          warn(f'Exiting due missing lock file on queue ID:{self.id}...')
          self.running = False
          break
        self.spawn()
        time.sleep(5)
    return self

  def stop(self) -> 'ScraperQueue':
    self.running = False
    return self