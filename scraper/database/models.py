import datetime
from typing import List
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
  pass

class ScrapedSite(Base):
  __tablename__ = 'scraped_sites'
  id: Mapped[int] = mapped_column(primary_key=True)
  url: Mapped[str] = mapped_column(String(1024))
  scraped_time: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now(datetime.UTC))
  # articles: Mapped[List['ScrapedArticle']] = relationship(back_populates='site_id', cascade='all, delete-orphan')

class ScrapedArticle(Base):
  __tablename__ = 'scraped_articles'
  id: Mapped[int] = mapped_column(primary_key=True)
  url_hash: Mapped[str] = mapped_column(String(64), unique=True)
  url: Mapped[str] = mapped_column(String(2000))
  site_id: Mapped[int] = mapped_column(ForeignKey('scraped_sites.id'))
  title: Mapped[str] = mapped_column(String(500))
  content: Mapped[str] = mapped_column(String())
  author: Mapped[str] = mapped_column(String(100))
  published_time: Mapped[datetime.datetime] = mapped_column(DateTime)
  # site: Mapped['ScrapedSite'] = relationship(back_populates='articles')