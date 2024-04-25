from pprint import pprint
from typing import List, Type
from .scraper_article import ScraperArticle
from .commands import GenerateURLsCallbackType, ScrapeUrlsCallbackType, ScrapeArticleCallbackType, ScrapeJSONCallbackType
from .commands import Command, URLSpreadCommand, SoupRequestCommand, ParserCommand, URLGeneratorCommand, JSONRequestCommand

class Scraper:
  def __init__(self, base_url:str, refresh_interval_sec:int = 120) -> None:
    self.base_url = base_url
    self.refresh_interval_sec = refresh_interval_sec
    self.rss_urls:List[str] = []
    self.json_urls:List[str] = []
    self.page_urls:List[str] = []
    self.content_urls:List[str] = []
    self.commands:List[Command] = []
    self.articles:List[ScraperArticle] = []

  @classmethod
  def create(cls, base_url: str, refresh_interval_sec:int = 120) -> 'Scraper':
    return cls(base_url, refresh_interval_sec)

  def generate_json_urls(self, func: GenerateURLsCallbackType) -> 'Scraper':
    cmd = URLGeneratorCommand(self, func=func, list_name='json_urls')
    self.commands.append(cmd)
    return self

  def generate_rss_urls(self, func: GenerateURLsCallbackType) -> 'Scraper':
    cmd = URLGeneratorCommand(self, func=func, list_name='rss_urls')
    self.commands.append(cmd)
    return self

  def generate_page_urls(self, func: GenerateURLsCallbackType) -> 'Scraper':
    cmd = URLGeneratorCommand(self, func=func, list_name='page_urls')
    self.commands.append(cmd)
    return self

  def parse_json_urls(self, func: ScrapeJSONCallbackType) -> 'Scraper':
    cmd = URLSpreadCommand(self, cmdClass=JSONRequestCommand, spread_url_list='json_urls', func=func, list_name='content_urls')
    self.commands.append(cmd)
    return self

  def parse_rss_urls(self, func: ScrapeUrlsCallbackType) -> 'Scraper':
    for url in self.rss_urls:
      cmd = SoupRequestCommand(self, url, func=func, file_extension='xml', parser='lxml-xml', list_name='content_urls')
      self.commands.append(cmd)
    return self

  def parse_page_urls(self, func: ScrapeUrlsCallbackType) -> 'Scraper':
    for url in self.page_urls:
      cmd = SoupRequestCommand(self, url, func=func, file_extension='html', parser='html.parser', list_name='content_urls')
      self.commands.append(cmd)
    return self

  def parse_article_content(self, func: ScrapeArticleCallbackType) -> 'Scraper':
    for url in self.content_urls:
      cmd = ParserCommand(self, url, func=func)
      self.commands.append(cmd)
    return self

  def debug(self) -> 'Scraper':
    print('\n---- DEBUG START ----\n')

    ## print urls
    for key in ['json_urls', 'rss_urls', 'page_urls', 'content_urls']:
      url_list = '\n'.join(getattr(self, key))
      print(f'\n### {key.upper()}:\n{url_list}')
      if len(url_list) == 0:
        print('-> Empty list\n')

    ## print command class names in self.commands
    cmd_list = '\n'.join([cmd.__class__.__name__ for cmd in self.commands])
    print(f'\n### COMMANDS:\n{cmd_list}')
    print('\n---- DEBUG END ----\n')
    return self

  def write_articles_to_db(self) -> 'Scraper':
    # write articles to a database
    return self

  def run(self) -> 'Scraper':
    for command in self.commands:
      command.execute()
    return self

  def queue(self) -> 'Scraper':
    # add current Scraper instance to a queue
    pass