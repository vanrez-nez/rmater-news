from datetime import datetime
from base.logger import log
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

class Scraper:
  def __init__(self, base_url:str, refresh_interval_sec:int = 60*5) -> None:
    self.base_url = base_url
    self.refresh_interval_sec = refresh_interval_sec
    self.last_run:float = 0
    self.running:bool = False
    self.xml_urls:List[str] = []
    self.json_urls:List[str] = []
    self.page_urls:List[str] = []
    self.content_urls:List[str] = []
    self.commands:List[Command] = []
    self.articles:List[ScraperArticle] = []

  def time_since_last_run(self) -> float:
    return (datetime.now() - get_last_scraped_time(self.base_url)).total_seconds()

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

  def run(self) -> 'Scraper':
    if self.running:
      return self
    log(f"Running Scraper for {self.base_url}")
    self.running = True
    for command in self.commands:
      command.execute()
    self.running = False
    return self