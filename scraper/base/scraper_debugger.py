def print_urls(scraper):
  for key in ['json_urls', 'xml_urls', 'page_urls', 'content_urls']:
    url_list = '\n'.join(getattr(scraper, key))
    print(f'\n### {key.upper()}:\n{url_list}')
    if len(url_list) == 0:
      print('-> Empty list\n')

def print_commands(scraper):
  cmd_list = '\n'.join([cmd.__class__.__name__ for cmd in scraper.commands])
  print(f'\n### COMMANDS:\n{cmd_list}')

def print_articles(scraper):
  articles = '\n\n'.join([str(article) for article in scraper.articles])
  print(f'\n### ARTICLES:\n{articles}')

def print_start():
  print('\n---- DEBUG START ----\n')

def print_end():
  print('\n---- DEBUG END ----\n')