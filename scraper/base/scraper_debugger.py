from base.logger import log

def print_urls(scraper):
  for key in ['json_urls', 'xml_urls', 'page_urls', 'content_urls']:
    url_list = '\n'.join(getattr(scraper, key))
    log(f'\n### {key.upper()}:\n{url_list}')
    if len(url_list) == 0:
      log('-> Empty list\n')

def print_commands(scraper):
  cmd_list = '\n'.join([cmd.__class__.__name__ for cmd in scraper.commands])
  log(f'\n### COMMANDS:\n{cmd_list}')

def print_articles(scraper):
  articles = '\n\n'.join([str(article) for article in scraper.articles])
  log(f'\n### ARTICLES:\n{articles}')

def print_start():
  log('\n---- DEBUG START ----\n')

def print_end():
  log('\n---- DEBUG END ----\n')