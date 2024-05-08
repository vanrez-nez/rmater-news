import os
import time
from base.logger import log

CACHE_DIR = "cache"

def prune_cache_files(time_since_creation=3600*24*30) -> None:
  log(f'Pruning cache files older than {time_since_creation/3600} hours')
  # scan cache directory for files
  for file in os.listdir(CACHE_DIR):
    file_path = os.path.join(CACHE_DIR, file)
    # check if file is older than time_since_creation
    if time.time() - os.path.getctime(file_path) > time_since_creation:
      os.remove(file_path)
      log(f'Removed {file_path}')