import os
import time
import requests
import hashlib
from base.logger import log
from base.logger import debug

CACHE_DIR = "cache"

def get_url(url, cache_duration=3600, extension='', cache=True):

  if not extension:
    extension = 'data'

  # Ensure the cache directory exists
  if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

  # Use a hash function for a consistent, positive hash
  url_hash = hashlib.md5(url.encode()).hexdigest()
  cache_file = f"{CACHE_DIR}/{url_hash}.{extension}"

  # remove cache file if it exists
  if not cache and os.path.exists(cache_file):
    os.remove(cache_file)

  # Check if cached file exists and is within the expiry time
  if os.path.exists(cache_file) and time.time() - os.path.getmtime(cache_file) < cache_duration:
    with open(cache_file, 'r', encoding='utf-8') as file:
      return file.read()

  # Make the full request and cache the result
  debug(f"URL Hash: {url_hash}")
  log(f"Req: {url}")
  response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
  response.encoding = 'utf-8'
  if response.status_code == 200:
    with open(cache_file, 'w', encoding='utf-8') as file:
      file.write(response.text)
    return response.text
  else:
    raise Exception(f"Request failed with status code {response.status_code}")

if __name__ == "__main__":
  # Example usage
  data = get_url("https://api.example.com/data")
