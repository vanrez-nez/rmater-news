import datetime
import urllib.parse
import hashlib

class ScraperArticle:
  def __init__(self) -> None:
    self.title:str = ''
    self.url:str = ''
    self.published_time:datetime.datetime = None
    self.author:str = ''
    self.content:str = ''

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