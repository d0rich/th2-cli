import requests

def get_file(url: str) -> str:
  response = requests.get(url)
  response.close()
  return response.content