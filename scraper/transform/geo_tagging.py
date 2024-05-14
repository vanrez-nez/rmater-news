import os
import json
from ollama import AsyncClient
from base.types import ScraperArticleType
from base.logger import log
from base.async_utils import async_wrapper
from database.db_handler import get_articles_without_location
from transform.prompts.geo_location import build_prompt
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama

cached_llm = None
glossary_contents = None
folder_path = 'storage/db'
embeddings = FastEmbedEmbeddings()
text_splitter = RecursiveCharacterTextSplitter(
  chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False
)

raw_prompt = PromptTemplate.from_template(
    """
    <s>[INST] Eres un asistente de ubicaciones para Mexico. Analiza los mensajes e intenta extraer su ubicacion.[/INST] </s>
    [INST] {input}
           Context: {context}
           Answer:
    [/INST]
"""
)

def load_llm():
  global cached_llm
  if (cached_llm is None):
    host = os.environ.get("OLLAMA_HOST")
    cached_llm = Ollama(base_url=host, model='llama3')

@async_wrapper
def load_glossary():
  global glossary_contents
  if (glossary_contents is None):
    file = 'storage/glossary.txt'
    print(f'Loading glossary from {file}')
    loader = TextLoader(file, 'utf-8')
    docs = loader.load_and_split()
    print(f'Loaded {len(docs)} documents')
    chunks = text_splitter.split_documents(docs)
    print(f'Split into {len(chunks)} chunks')
    vector_store = Chroma.from_documents(
      documents=chunks,
      embedding=embeddings,
      persist_directory=folder_path
    )
    glossary_contents = True

def get_articles() -> list[ScraperArticleType]:
  return get_articles_without_location(1)

@async_wrapper
def query_ollama(article: ScraperArticleType) -> dict:
  # host = os.environ.get("OLLAMA_HOST")
  # client = AsyncClient(host=host)
  load_llm()
  # await load_glossary()
  print('glosary loaded')
  prompt = build_prompt(article.title, article.content)
  vector_store = Chroma(persist_directory=folder_path, embedding_function=embeddings)
  retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
      "k": 20,
      "score_threshold": 0.1,
    },
  )

  document_chain = create_stuff_documents_chain(cached_llm, raw_prompt)
  chain = create_retrieval_chain(retriever, document_chain)
  result = chain.invoke({
    "input": prompt
  })
  response = result['answer']
  print(result)
  return response

async def run():
  articles = get_articles()
  for article in articles:
    response = await query_ollama(article)
    try:
      content = response #.get('message', {}).get('content', {})
      json_response = json.loads(content)
      # validate response and required fields
      fields = ['pais', 'estado', 'ciudad', 'municipio', 'asentamiento', 'calle', 'numero', 'lugar']
      if not all(field in json_response for field in fields):
        log('Invalid response', json_response)
        continue
      log(f'{article.url}, Valid response {json_response}')
    except:
      log('Invalid JSON response', response)
      continue

    # log('Pais', json_response['pais'])
    # log('Estado', json_response['estado'])
    # log('Ciudad', json_response['ciudad'])
    # log('Municipio', json_response['municipio'])
    # log('Colonia', json_response['colonia'])
