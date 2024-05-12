import asyncio
from datetime import datetime
from base.logger import log, warn
from typing import List
from base.scraper_article import ScraperArticle
from base.commands import GenerateURLsCallbackType, ScrapeUrlsCallbackType, ScrapeArticleCallbackType, ScrapeJSONCallbackType
from base.commands import Command
from base.commands import SpreadListCommand
from base.commands import SoupRequestCommand
from base.commands import ParserCommand
from base.commands import URLGeneratorCommand
from base.commands import JSONRequestCommand
from base.commands import WriteArticlesCommand
from base.commands import DebugCommand
from database.db_handler import get_last_scraped_time
from base.async_utils import async_wrapper

class Scraper:
  def __init__(self, base_url:str, refresh_interval_sec:int = 60*5) -> None:
    self.base_url = base_url
    self.refresh_interval_sec = refresh_interval_sec
    self.last_run_time:datetime = datetime.now()
    self.task_running:bool = asyncio.Event()
    self.xml_urls:List[str] = []
    self.json_urls:List[str] = []
    self.page_urls:List[str] = []
    self.content_urls:List[str] = []
    self.commands:List[Command] = []
    self.articles:List[ScraperArticle] = []

  @property
  def running(self) -> bool:
    return self.task_running.is_set()

  @property
  def time_since_last_run(self) -> float:
    if (self.running): return 0
    return (datetime.now() - self.last_run_time).total_seconds()

  @async_wrapper
  def sync_last_run_time(self) -> None:
    self.last_run_time = get_last_scraped_time(self.base_url)

  def merge_to(self, list_name: str, new_list: List[str]) -> 'Scraper':
    current_list = getattr(self, list_name)
    setattr(self, list_name, list(set(current_list) | set(new_list)))
    return self

  def generate_json_urls(self, func: GenerateURLsCallbackType) -> 'Scraper':
    cmd = URLGeneratorCommand(self, func=func, list_name='json_urls')
    self.commands.append(cmd)
    return self

  def generate_xml_urls(self, func: GenerateURLsCallbackType) -> 'Scraper':
    cmd = URLGeneratorCommand(self, func=func, list_name='xml_urls')
    self.commands.append(cmd)
    return self

  def generate_page_urls(self, func: GenerateURLsCallbackType) -> 'Scraper':
    cmd = URLGeneratorCommand(self, func=func, list_name='page_urls')
    self.commands.append(cmd)
    return self

  def parse_json_urls(self, func: ScrapeJSONCallbackType) -> 'Scraper':
    cmd = SpreadListCommand(self, cmdClass=JSONRequestCommand, spread_list='json_urls',
                          param_name='url', func=func, list_name='content_urls', cache_duration=60)
    self.commands.append(cmd)
    return self

  def parse_xml_urls(self, func: ScrapeUrlsCallbackType) -> 'Scraper':
    cmd = SpreadListCommand(self, cmdClass=SoupRequestCommand, spread_list='xml_urls',
                          param_name='url', func=func, list_name='content_urls',
                          file_extension='xml', parser='lxml-xml', cache_duration=60)
    self.commands.append(cmd)
    return self

  def parse_page_urls(self, func: ScrapeUrlsCallbackType) -> 'Scraper':
    cmd = SpreadListCommand(self, cmdClass=SoupRequestCommand, spread_list='page_urls',
                          param_name='url', func=func, list_name='content_urls',
                          file_extension='hml', parser='html.parser', cache_duration=60)
    self.commands.append(cmd)
    return self

  def parse_article_content(self, func: ScrapeArticleCallbackType) -> 'Scraper':
    cmd = SpreadListCommand(self, cmdClass=ParserCommand, param_name='url', spread_list='content_urls', func=func)
    self.commands.append(cmd)
    return self

  def debug(self) -> 'Scraper':
    cmd = DebugCommand(self)
    self.commands.append(cmd)
    return self

  def write_articles_to_db(self) -> 'Scraper':
    cmd = WriteArticlesCommand(self)
    self.commands.append(cmd)
    return self

  async def run(self) -> 'Scraper':
    if self.running:
      return self
    warn(f"Running Scraper for {self.base_url}")
    self.task_running.set()
    try:
      self.articles = []
      self.xml_urls = []
      self.json_urls = []
      self.page_urls = []
      self.content_urls = []
      for cmd in self.commands:
        await cmd.execute()
    except Exception as e:
      log(f"Error running scraper for {self.base_url}: {e}")
    finally:
      self.last_run_time = datetime.now()
      self.task_running.clear()
    warn(f"Scrapper Finished for {self.base_url}")
    return self