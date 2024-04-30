import datetime
from typing import Callable, Type
from bs4 import BeautifulSoup
from base.types import ScraperType
from base.types import ScrapeUrlsCallbackType, ScrapeJSONCallbackType, ScrapeArticleCallbackType, GenerateURLsCallbackType
from base.request import get_url
from base.json_search import JSONSearch
from base.scraper_article import ScraperArticle
from base.url_generator import URLGenerator
from database.db_handler import write_articles

class Command:
  def execute(self):
    raise NotImplementedError

class SoupFetcher:
  """Partial used to fetch a URL and parse it with BeautifulSoup"""
  def __init__(self, url: str, cache_duration: int = 3600*24*30, file_extension: str = '', parser: str = 'html.parser'):
    self.url = url
    self.cache_duration = cache_duration
    self.file_extension = file_extension
    self.parser = parser

  def fetch_and_parse(self):
    content = get_url(self.url, self.cache_duration, extension=self.file_extension)
    return BeautifulSoup(content, self.parser)

class JSONFetcher:
  """Partial used to fetch JSON data from a URL in a command"""
  def __init__(self, url: str, cache_duration: int = 3600*24*30):
    self.url = url
    self.cache_duration = cache_duration

  def fetch_and_parse(self):
    content = get_url(self.url, self.cache_duration, extension='json')
    return JSONSearch(content)

class URLGeneratorCommand(Command):
  """Command to generate URLs using a URLGenerator"""
  def __init__(self, scraper: ScraperType, list_name: str, func: GenerateURLsCallbackType):
    self.func = func
    self.scraper = scraper
    self.list_name = list_name
    self.generator = URLGenerator.create()

  def execute(self):
    setattr(self.scraper, self.list_name, self.func(self.scraper, self.generator))

class ParserCommand(Command):
  """Command to parse an article using a callback function"""
  def __init__(self, scraper: ScraperType, url: str, func: ScrapeArticleCallbackType, **kwargs):
    self.fetcher = SoupFetcher(url, **kwargs)
    self.scraper = scraper
    self.func = func

  def execute(self):
    soup = self.fetcher.fetch_and_parse()
    article = ScraperArticle()
    article.title = soup.select_one('h1').getText(strip=True)
    article.url = self.fetcher.url
    article.published_time = datetime.datetime.now()
    self.func(self.scraper, soup, article)
    self.scraper.articles.append(article)

class JSONRequestCommand(Command):
  """Command to fetch JSON data and parse it using a callback function"""
  def __init__(self, scraper: ScraperType, url: str, list_name:str, func: ScrapeJSONCallbackType, **kwargs):
    self.fetcher = JSONFetcher(url, **kwargs)
    self.scraper = scraper
    self.func = func
    self.list_name = list_name

  def execute(self):
    json_search = self.fetcher.fetch_and_parse()
    new_lst = self.func(self.scraper, json_search)
    self.scraper.merge_to(self.list_name, new_lst)

class SpreadListCommand(Command):
  """This command is used to spread a list of values as a parameter into each command class"""
  def __init__(self, scraper: ScraperType, cmdClass: Type[Command], spread_list:str, param_name:str, **kwargs):
    self.scraper = scraper
    self.spread_list = spread_list
    self.cmdClass = cmdClass
    self.param_name = param_name
    self.args = kwargs

  def execute(self):
    lst = getattr(self.scraper, self.spread_list)
    for val in lst:
      self.cmdClass(self.scraper, **{self.param_name:val}, **self.args).execute()

class SoupRequestCommand(Command):
  """This command is used to fetch a url and parse it with BeautifulSoup"""
  def __init__(self, scraper: ScraperType, url: str, list_name:str, func: ScrapeUrlsCallbackType, **kwargs):
    self.fetcher = SoupFetcher(url, **kwargs)
    self.scraper = scraper
    self.func = func
    self.list_name = list_name

  def execute(self):
    soup = self.fetcher.fetch_and_parse()
    new_lst = self.func(self.scraper, soup)
    self.scraper.merge_to(self.list_name, new_lst)

class WriteArticlesCommand(Command):
  """Command to write articles to the database"""
  def __init__(self, scraper: ScraperType):
    self.scraper = scraper

  def execute(self):
    write_articles(self.scraper.articles)