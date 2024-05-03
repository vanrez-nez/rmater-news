import os
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from base.types import ScraperArticleType
from database.models import ScrapedArticle
from database.models import ScrapedSite
from database.models import Base

db_path = os.path.join(os.path.dirname(__file__), '..', 'storage/scraper.db')
engine = create_engine(f'sqlite:///{db_path}', future=True, echo=False)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def get_last_scraped_time(url: str) -> datetime.datetime:
  session = Session()
  site = session.query(ScrapedSite).filter_by(url=url).first()
  session.close()
  if site:
    return site.scraped_time
  return None

def write_articles(articles: list[ScraperArticleType]) -> bool:
  session = Session()
  try:
    for a in articles:
      site = session.query(ScrapedSite).filter_by(url=a.site_url).first()
      if not site:
        site = ScrapedSite(url=a.site_url)
        session.add(site)
      site.scraped_time = datetime.datetime.now(datetime.UTC)

      article = session.query(ScrapedArticle).filter_by(url_hash=a.url_hash).first()
      if article:
        # update article
        article.title = a.title
        article.site_id = site.id
        article.url = a.url
        article.author = a.author
        article.content = a.content
        article.published_time = a.published_time
      else:
        session.add(ScrapedArticle(
          url_hash=a.url_hash,
          title=a.title,
          site_id=site.id,
          url=a.url,
          author=a.author,
          content=a.content,
          published_time=a.published_time
        ))
    session.commit()
  except:
    session.rollback()
    return False
  finally:
    session.close()
    return True