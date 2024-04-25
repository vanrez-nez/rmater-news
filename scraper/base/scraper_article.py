from dataclasses import dataclass

@dataclass
class ScraperArticle:
    title: str
    url: str
    date: str
    author: str
    content: str