import datetime
import urllib.parse
import hashlib
from base.serialize import SerializableDict

class ScraperArticle(SerializableDict):
  def __init__(self, fields: dict = None) -> None:
    fields = fields or {}
    self.title:str = fields.get('title', '')
    self.url:str = fields.get('url', '')
    self.published_time:datetime.datetime = fields.get('published_time', None)
    self.author:str = fields.get('author', '')
    self.content:str = fields.get('content', '')
    super().__init__(self.__dict__)

  @property
  def site_url(self) -> str:
    parsed_url = urllib.parse.urlparse(self.url)
    site_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return site_url

  @property
  def url_hash(self) -> str:
    return hashlib.sha256(self.url.encode('utf-8')).hexdigest()

  def __repr__(self) -> str:
    return f'{self.url}\n > Date: {self.published_time}\n > Title: {self.title}\n > Author: {self.author}\n > Content: {self.content[:120]}...'