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
from base.scraper_debugger import print_start, print_end, print_urls, print_articles, print_commands

class Scraper:
  def __init__(self, base_url:str, refresh_interval_sec:int = 120) -> None:
    self.base_url = base_url
    self.refresh_interval_sec = refresh_interval_sec
    self.xml_urls:List[str] = []
    self.json_urls:List[str] = []
    self.page_urls:List[str] = []
    self.content_urls:List[str] = []
    self.commands:List[Command] = []
    self.articles:List[ScraperArticle] = []

  @classmethod
  def create(cls, base_url: str, refresh_interval_sec:int = 120) -> 'Scraper':
    return cls(base_url, refresh_interval_sec)

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
                          param_name='url', func=func, list_name='content_urls')
    self.commands.append(cmd)
    return self

  def parse_xml_urls(self, func: ScrapeUrlsCallbackType) -> 'Scraper':
    cmd = SpreadListCommand(self, cmdClass=SoupRequestCommand, spread_list='xml_urls',
                          param_name='url', func=func, list_name='content_urls', file_extension='xml', parser='lxml-xml')
    self.commands.append(cmd)
    return self

  def parse_page_urls(self, func: ScrapeUrlsCallbackType) -> 'Scraper':
    cmd = SpreadListCommand(self, cmdClass=SoupRequestCommand, spread_list='page_urls',
                          param_name='url', func=func, list_name='content_urls', file_extension='hml', parser='html.parser')
    self.commands.append(cmd)
    return self

  def parse_article_content(self, func: ScrapeArticleCallbackType) -> 'Scraper':
    cmd = SpreadListCommand(self, cmdClass=ParserCommand, param_name='url', spread_list='content_urls', func=func)
    self.commands.append(cmd)
    return self

  def debug(self) -> 'Scraper':
    print_start()
    print_urls(self)
    print_articles(self)
    print_commands(self)
    print_end()
    return self

  def write_articles_to_db(self) -> 'Scraper':
    cmd = WriteArticlesCommand(self)
    self.commands.append(cmd)
    return self

  def run(self) -> 'Scraper':
    for command in self.commands:
      command.execute()
    return self

  def queue(self) -> 'Scraper':
    # add current Scraper instance to a queue
    pass