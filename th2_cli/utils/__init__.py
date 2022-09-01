import requests
import yaml


def get_file(url: str) -> str:
    response = requests.get(url)
    response.close()
    return response.content


def get_yaml_config(url: str):
    yaml_text = get_file(url)
    return yaml.safe_load_all(yaml_text)
