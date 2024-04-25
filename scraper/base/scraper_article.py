from dataclasses import dataclass

class ScraperArticle:
  def __init__(self) -> None:
    self.title = ''
    self.url = ''
    self.date = ''
    self.author = ''
    self.content = ''

  def __repr__(self) -> str:
    return f'{self.url}\n > Date: {self.date}\n > Title: {self.title}\n > Author: {self.author}\n > Content: {self.content[:120]}...'