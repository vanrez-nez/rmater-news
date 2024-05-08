import datetime
import enum
from typing import List
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String
from sqlalchemy import SmallInteger
from sqlalchemy import Numeric
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
  pass

class Site(Base):
  __tablename__ = 'sites'
  id: Mapped[int] = mapped_column(primary_key=True)
  url: Mapped[str] = mapped_column(String(1024))
  scraped_time: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now(datetime.UTC))
  articles: Mapped[List['Article']] = relationship('Article', back_populates='site')

class Article(Base):
  __tablename__ = 'articles'
  id: Mapped[int] = mapped_column(primary_key=True)
  url_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
  url: Mapped[str] = mapped_column(String(2000), nullable=False)
  site_id: Mapped[int] = mapped_column(ForeignKey('sites.id'), nullable=False)
  title: Mapped[str] = mapped_column(String(500), nullable=False)
  content: Mapped[str] = mapped_column(String(), nullable=False)
  transformed_title: Mapped[str] = mapped_column(String(500), nullable=True)
  transformed_content: Mapped[str] = mapped_column(String(), nullable=True)
  author: Mapped[str] = mapped_column(String(100))
  published_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
  site: Mapped['Site'] = relationship('Site', back_populates='articles')
  locations: Mapped[List['Location']] = relationship('Location', secondary='article_locations', back_populates='articles')
  tags: Mapped[List['Tag']] = relationship('Tag', secondary='article_tags', back_populates='articles')

class LocationType(enum.Enum):
  country = 'country'
  city = 'city'
  region = 'region'
  address = 'address'

class Location(Base):
  __tablename__ = 'locations'
  id: Mapped[str] = mapped_column(String(64), primary_key=True)
  name: Mapped[str] = mapped_column(String(100))
  type: Mapped[LocationType] = mapped_column(Enum(LocationType))
  latitude: Mapped[float] = mapped_column(Numeric(9, 6))
  longitude: Mapped[float] = mapped_column(Numeric(9, 6))
  articles: Mapped[List['Article']] = relationship('Article', secondary='article_locations', back_populates='locations')

class ArticleLocation(Base):
  __tablename__ = 'article_locations'
  article_id: Mapped[int] = mapped_column(ForeignKey('articles.id'), primary_key=True)
  location_id: Mapped[str] = mapped_column(ForeignKey('locations.id'), primary_key=True)

class ArticleTag(Base):
  __tablename__ = 'article_tags'
  article_id: Mapped[int] = mapped_column(ForeignKey('articles.id'), primary_key=True)
  tag_id: Mapped[int] = mapped_column(ForeignKey('tags.id'), primary_key=True)

class Tag(Base):
  __tablename__ = 'tags'
  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(100), unique=True)
  description: Mapped[str] = mapped_column(String())
  articles: Mapped[List['Article']] = relationship('Article', secondary='article_tags', back_populates='tags')

class Queue(Base):
  __tablename__ = 'queue'
  id: Mapped[int] = mapped_column(primary_key=True)
  channel: Mapped[str] = mapped_column(String(100))
  job: Mapped[str] = mapped_column(String())
  priority: Mapped[int] = mapped_column(SmallInteger, default=0)
  attempt: Mapped[int] = mapped_column(SmallInteger, default=0)
  progress: Mapped[int] = mapped_column(SmallInteger, default=0)
  time_pushed: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now(datetime.UTC))
  time_error: Mapped[datetime.datetime] = mapped_column(DateTime)