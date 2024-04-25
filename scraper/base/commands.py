from typing import Callable, List, Any, Type
from .request import get_url
from bs4 import BeautifulSoup
from .json_search import JSONSearch
from .scraper_article import ScraperArticle
from .url_generator import URLGenerator

ScrapeUrlsCallbackType = Callable[[BeautifulSoup], List[str]]
ScrapeJSONCallbackType = Callable[[JSONSearch], List[str]]
ScrapeArticleCallbackType = Callable[[BeautifulSoup, ScraperArticle], None]
GenerateURLsCallbackType = Callable[[URLGenerator], List[str]]
GenericListCallbackType = Callable[[], List[str]]

class Command:
  def execute(self):
    raise NotImplementedError

class URLSpreadCommand(Command):
  def __init__(self, scraper, cmdClass: Type[Command], spread_url_list:str, **kwargs):
    self.scraper = scraper
    self.spread_url_list = spread_url_list
    self.cmdClass = cmdClass
    self.args = kwargs

  def execute(self):
    urls = getattr(self.scraper, self.spread_url_list)
    for url in urls:
      self.cmdClass(self.scraper, url=url, **self.args).execute()

class SoupFetcher:
  def __init__(self, url: str, cache_duration: int = 3600*24*30, file_extension: str = '', parser: str = 'html.parser'):
    self.url = url
    self.cache_duration = cache_duration
    self.file_extension = file_extension
    self.parser = parser

  def fetch_and_parse(self):
    content = get_url(self.url, self.cache_duration, extension=self.file_extension)
    return BeautifulSoup(content, self.parser)

class JSONFetcher:
  def __init__(self, url: str, cache_duration: int = 3600*24*30):
    self.url = url
    self.cache_duration = cache_duration

  def fetch_and_parse(self):
    content = get_url(self.url, self.cache_duration, extension='json')
    return JSONSearch(content)

class URLGeneratorCommand(Command):
  def __init__(self, scraper, list_name: str, func: GenerateURLsCallbackType):
    from base.scraper import Scraper
    self.func = func
    self.scraper:Scraper = scraper
    self.list_name = list_name
    self.generator = URLGenerator.create()

  def execute(self):
    setattr(self.scraper, self.list_name, self.func(self.generator))

class ParserCommand(Command):
  def __init__(self, scraper: Any, url: str, func: ScrapeArticleCallbackType, **kwargs):
    from base.scraper import Scraper
    self.fetcher = SoupFetcher(url, **kwargs)
    self.scraper:Scraper = scraper
    self.func = func

  def execute(self):
    soup = self.fetcher.fetch_and_parse()
    article = ScraperArticle()
    self.func(soup, article)
    self.scraper.articles.append(article)

class JSONRequestCommand(Command):
  def __init__(self, scraper, url: str, list_name:str, func: ScrapeJSONCallbackType, **kwargs):
    self.fetcher = JSONFetcher(url, **kwargs)
    self.scraper = scraper
    self.func = func
    self.list_name = list_name

  def execute(self):
    json_search = self.fetcher.fetch_and_parse()
    current_lst = getattr(self.scraper, self.list_name)
    new_lst = self.func(json_search)
    lst = list(set(current_lst) | set(new_lst))
    setattr(self.scraper, self.list_name, lst)


class SoupRequestCommand(Command):
  def __init__(self, scraper, url: str, list_name:str, func: ScrapeUrlsCallbackType, **kwargs):
    self.fetcher = SoupFetcher(url, **kwargs)
    self.scraper = scraper
    self.func = func
    self.list_name = list_name

  def execute(self):
    soup = self.fetcher.fetch_and_parse()
    setattr(self.scraper, self.list_name, self.func(soup))
