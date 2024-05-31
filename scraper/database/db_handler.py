import os
import datetime
from base.logger import error
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy import func
from base.types import ScraperArticleType
from base.types import ArticleLocationType
from database.models import Article
from database.models import Site
from database.models import Base
from database.models import Location

db_path = os.path.join(os.path.dirname(__file__), '..', 'storage/scraper.db')
engine = create_engine(f'sqlite:///{db_path}', future=True, echo=False)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def get_last_scraped_time(url: str) -> datetime.datetime:
  session = Session()
  site = session.query(Site).filter_by(url=url).first()
  session.close()
  if site:
    return site.scraped_time
  return datetime.datetime.min

def get_articles_without_location(limit: int) -> list[Article]:
  session = Session()
  # sort by published_time
  articles = (session
              .query(Article)
              .order_by(desc(func.date(Article.published_time)))
              .filter(Article.locations == None)
              .limit(limit)
              .all()
            )
  session.close()
  return articles

def write_location(scraperArticle: ScraperArticleType, articleLocation: ArticleLocationType ) -> bool:
  session = Session()
  try:
    article = session.query(Article).filter_by(url=scraperArticle.url).first()
    location = session.query(Location).filter_by(id=articleLocation.id).first()
    if not article:
      error(f"Article not found: {scraperArticle.url}")
      return False
    if not location:
      location = Location(
        id=articleLocation.id,
        name=articleLocation.name,
        rank_address=articleLocation.rank_address,
        latitude=articleLocation.lat,
        longitude=articleLocation.lon
      )
      session.add(location)
    # check if locations already exists in article
    if not location in article.locations:
      article.locations.append(location)
      session.commit()
  except Exception as e:
    error("@write_location error:", e)
    session.rollback()
    return False
  finally:
    session.close()
    return True

def write_articles(articles: list[ScraperArticleType]) -> bool:
  session = Session()
  try:
    for a in articles:
      site = session.query(Site).filter_by(url=a.site_url).first()
      if not site:
        site = Site(url=a.site_url)
        session.add(site)
      site.scraped_time = datetime.datetime.now(datetime.UTC)

      article = session.query(Article).filter_by(url_hash=a.url_hash).first()
      if article:
        # update article
        article.title = a.title
        article.site_id = site.id
        article.url = a.url
        article.author = a.author
        article.content = a.content
        article.published_time = a.published_time
      else:
        session.add(Article(
          url_hash=a.url_hash,
          title=a.title,
          site_id=site.id,
          url=a.url,
          author=a.author,
          content=a.content,
          published_time=a.published_time
        ))
    session.commit()
  except Exception as e:
    error("write_articles error:", e)
    session.rollback()
    return False
  finally:
    session.close()
    return True