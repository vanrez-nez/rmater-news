import os
from ollama import Client

def run():
  host = os.environ.get("OLLAMA_HOST")
  client = Client(host=host)
  response = client.chat(model='llama3', messages=[
    {
      'role': 'user',
      'content': 'Why is the sky blue?',
    },
  ])
  print(response)