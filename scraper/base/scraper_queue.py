import asyncio
import aiofiles
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
    self.max_running_scrapers: int = 5
    log(f"New Queue ID: {self.id} - OS PID: {os.getpid()}")

  @property
  def running_count(self) -> int:
    return len([s for s in self.queue if s.running])

  async def write_lock_file(self) -> None:
    async with aiofiles.open('queue.lock', 'w') as f:
      await f.write(str(self.id))

  async def read_lock_file(self) -> str:
    async with aiofiles.open('queue.lock', 'r') as f:
      return await f.read()

  async def is_lock_active(self) -> bool:
    lock_id = await self.read_lock_file()
    return str(self.id) == lock_id

  def add(self, scraper: ScraperType|List[ScraperType]) -> 'ScraperQueue':
    scrapers = scraper if isinstance(scraper, list) else [scraper]
    for scraper in scrapers:
      # verify that scraper is not already in the queue by checking the base_url
      scraper_base_urls = [s.base_url for s in self.queue]
      if scraper.base_url not in scraper_base_urls:
        self.queue.append(scraper)
    return self

  async def sync_scrapers_time(self) -> 'ScraperQueue':
    for scraper in self.queue:
      await scraper.sync_last_run_time()
    return self

  async def get_pending(self) -> List[ScraperType]:
    scrapers = [s for s in self.queue if not s.running]
    scrapers = [s for s in scrapers if s.time_since_last_run > s.refresh_interval_sec]
    return scrapers[:self.max_running_scrapers - self.running_count]

  async def spawn(self) -> 'ScraperQueue':
    scrapers = await self.get_pending()
    if not scrapers:
      return self
    log(f"Running {len(scrapers)} scrapers on queue ID:{self.id}...")
    for scraper in scrapers:
      time_since_last_run = scraper.time_since_last_run
      log(f"{scraper.base_url}: {scraper.running} - {time_since_last_run}")
    # run all scrapers in the queue in parallel
    tasks = [scraper.run() for scraper in scrapers]
    await asyncio.gather(*tasks)
    return self

  async def start(self) -> 'ScraperQueue':
    await self.write_lock_file()
    await self.sync_scrapers_time()
    if not self.running:
      self.running = True
      while self.running:
        if not await self.is_lock_active():
          warn(f'Exiting due missing lock file on queue ID:{self.id}...')
          self.running = False
          break
        await asyncio.gather(*[self.spawn(), asyncio.sleep(1)])
    return self

  def stop(self) -> 'ScraperQueue':
    self.running = False
    return self