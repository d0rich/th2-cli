import requests
import os
import yaml


def get_file(path: str) -> str:
    if path.startswith('http'):
        response = requests.get(path)
        response.close()
        content = response.content
    else:
        file_path = os.path.abspath(
            os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir, path)
        )
        file = open(file_path)
        content = file.read()
    return content


def get_yaml_config(path: str):
    yaml_text = get_file(path)
    return yaml.safe_load_all(yaml_text)


def read_value(question: str, prompt: str = '', default_value: str = '') -> str:
    if bool(default_value):
        print(f'{question} (Default: "{default_value}")')
    else:
        print(question)
    value = input(f'{prompt}: ')
    if bool(value):
        return value
    else:
        return default_value


def is_ip(address: str) -> bool:
    return address.replace('.', '').isnumeric()


def write_file(name: str, content: any):
    f = open(name, "w")
    f.write(content)
    f.close()
