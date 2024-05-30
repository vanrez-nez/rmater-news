import os
import time
import aiohttp
import asyncio
import hashlib
from urllib.parse import urlencode
from aiofiles import open as aio_open
from base.logger import log, debug

CACHE_DIR = "cache"
semaphore = asyncio.Semaphore(5)  # Adjust the number to limit concurrent requests

async def make_request(url, cache_duration=3600, extension='', cache=True, form_data=None, method='GET'):
  if not extension:
    extension = 'data'

  # Ensure the cache directory exists
  if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

  # Use a hash function for a consistent, positive hash
  url_hash = hashlib.md5(url.encode()).hexdigest()
  cache_file = f"{CACHE_DIR}/{url_hash}.{extension}"

  # Remove cache file if it exists and caching is disabled
  if not cache and os.path.exists(cache_file):
    os.remove(cache_file)

  # Check if cached file exists and is within the expiry time
  if os.path.exists(cache_file) and time.time() - os.path.getmtime(cache_file) < cache_duration:
    async with aio_open(cache_file, 'r', encoding='utf-8') as file:
      return await file.read()

  # Make the full request and cache the result
  async with semaphore:
    async with aiohttp.ClientSession() as session:
      debug(f"URL Hash: {url_hash}")
      log(f"Req: {url}")
      timeout = aiohttp.ClientTimeout(total=60)
      f_data=None
      if form_data:
        f_data = aiohttp.FormData(form_data)
      async with session.request(
        url=url,
        method=method,
        timeout=timeout,
        data=f_data,
        headers={"User-Agent": "Mozilla/5.0"}
      ) as response:
        try:
          response_text = await response.text(encoding='utf-8')
        except Exception as e:
          response_text = await response.text(encoding='latin-1')
        if response.status == 200:
          if cache:
            async with aio_open(cache_file, 'w', encoding='utf-8') as file:
              await file.write(response_text)
          return response_text
        else:
          raise Exception(f"Request failed with status code {response.status}")


async def main():
  try:
    data = await make_request("https://api.example.com/data")
    print(data)
  except Exception as e:
    print(str(e))

if __name__ == "__main__":
  asyncio.run(main())
