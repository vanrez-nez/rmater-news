import emoji
import pytz
import re
from threading import Timer
from typing import List
from datetime import datetime, timedelta
from dateutil import parser
from bs4 import BeautifulSoup
from base.json_search import JSONSearch
from base.logger import warn

def strip_emoji(text: str|List[str]) -> str|list[str]:
  if isinstance(text, list):
    return [emoji.replace_emoji(t, ' ') for t in text]
  return emoji.replace_emoji(text, ' ')

def json_search_from_tag(soup: BeautifulSoup, selector: str = 'script[type="application/ld+json"]') -> JSONSearch:
  json_content = soup.select_one(selector).get_text(strip=True)
  # remove new lines causing JSON parsing errors
  json_content = re.sub(r'\n', '', json_content)
  return JSONSearch(json_content.strip().encode('utf-8'))

def normalize_iso_date(date_str: str, format: str, offset_hours: int = 0) -> str:
  date = datetime.strptime(date_str, format)
  if (offset_hours != 0):
    date = date + timedelta(hours=offset_hours)
  if date > datetime.now(pytz.utc):
    warn(f'Future date detected: {date_str}')
  return date.isoformat()

def iso_date_to_utc(date_str: str) -> str:
  date_str = date_str.replace('Z', '+00:00')
  date = parser.parse(date_str)
  return date.astimezone(pytz.utc)

def fix_punctuation_spaces(text: str) -> str:
  # remove double spaces
  text = re.sub(r'\s+', ' ', text)
  # remove space before punctuation using regex
  text = re.sub(r'\s+([,.])', r'\1', text)
  # trim spaces inside quotes
  text = re.sub(r'[“”‘’]', '"', text)
  text = re.sub(r'"(\s*)(.*?)(\s*)"', r'"\2"', text)
  # trim spaces inside parentheses
  text = re.sub(r'\((\s*)(.*?)(\s*)\)', r'(\2)', text)
  return text

def nodes_to_lines(nodes: list[BeautifulSoup], strip_emojis: bool = True) -> list[str]:
  lines = [node.get_text(strip=True, separator=' ') for node in nodes]
  if strip_emojis:
    lines = strip_emoji(lines)
  return lines

def join_lines(lines: list[str], fix_punctuation: bool = True) -> str:
  lines = ' '.join(lines)
  if fix_punctuation:
    lines = fix_punctuation_spaces(lines)
  return lines

def filter_lines_starting_with(lines: list[str], text: str|list[str]) -> list:
  removals = text if isinstance(text, list) else [text]
  for current in removals:
    lines = [line for line in lines if not line.strip().startswith(current)]
  return lines

def debounce(wait):
    """ Decorator that will postpone a functions
        execution until after wait seconds
        have elapsed since the last time it was invoked. """
    def decorator(fn):
        def debounced(*args, **kwargs):
            def call_it():
                fn(*args, **kwargs)
            try:
                debounced.t.cancel()
            except(AttributeError):
                pass
            debounced.t = Timer(wait, call_it)
            debounced.t.start()
        return debounced
    return decorator