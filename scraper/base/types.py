from __future__ import annotations
from typing import TYPE_CHECKING, Type, List, Callable
from bs4 import BeautifulSoup
from base.json_search import JSONSearch
from base.url_generator import URLGenerator
from entities.scraper_article import ScraperArticle
from entities.article_location import ArticleLocation

if TYPE_CHECKING:
  from .scraper import Scraper

ScraperType = Type['Scraper']
ArticleLocationType = Type[ArticleLocation]
ScraperArticleType = Type[ScraperArticle]
JSONSearchType = Type[JSONSearch]
BeautSoupType = Type[BeautifulSoup]
URLGeneratorType = Type[URLGenerator]
ScrapeUrlsCallbackType = Callable[[BeautifulSoup], List[str]]
ScrapeJSONCallbackType = Callable[[JSONSearch], List[str]]
ScrapeArticleCallbackType = Callable[[BeautifulSoup, ScraperArticle], None]
GenerateURLsCallbackType = Callable[[URLGenerator], List[str]]