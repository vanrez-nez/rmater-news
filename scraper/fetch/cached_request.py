import os
import time
import requests
import hashlib

CACHE_DIR = "cache"

def get_extension_from_headers(headers):
    content_type = headers.get('content-type', '')
    if 'json' in content_type:
        return '.json'
    elif 'xml' in content_type:
        return '.xml'
    elif 'html' in content_type:
        return '.html'
    else:
        return ''

def get_url(url, cache_duration=3600, extension=None, cache=True):
    # Ensure the cache directory exists
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    # Use a hash function for a consistent, positive hash
    url_hash = hashlib.md5(url.encode()).hexdigest()

    if extension is None:
        # Make an initial request to get the content type
        response = requests.head(url)
        extension = get_extension_from_headers(response.headers)

    cache_file = f"{CACHE_DIR}/{url_hash}.{extension}"

    # remove cache file if it exists
    if not cache and os.path.exists(cache_file):
        os.remove(cache_file)

    # Check if cached file exists and is within the expiry time
    if os.path.exists(cache_file) and time.time() - os.path.getmtime(cache_file) < cache_duration:
        with open(cache_file, 'rb') as file:
            return file.read()

    # Make the full request and cache the result
    print(f"Requesting {url}")
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code == 200:
        with open(cache_file, 'wb') as file:
            file.write(response.content)
        return response.content
    else:
        raise Exception(f"Request failed with status code {response.status_code}")


if __name__ == "__main__":
    # Example usage
    data = get_url("https://api.example.com/data")