import requests
import os
import yaml
from typing import Iterator
from colorama import Fore, Back, Style


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


def get_yaml_config(path: str) -> Iterator[dict]:
    yaml_text = get_file(path)
    return yaml.safe_load_all(yaml_text)


def print_info(message):
    print(f'{Fore.BLUE}{message}{Style.RESET_ALL}')


def print_error(message):
    print(f'{Fore.RED}{message}{Style.RESET_ALL}')


def read_value(question: str, prompt: str = '', default_value: str = '') -> str:
    if bool(default_value):
        print(f'{question} {Style.DIM}(Default: "{default_value}"){Style.RESET_ALL}')
    else:
        print(question)
    value = input(f'{prompt}: {Fore.CYAN}')
    print(Style.RESET_ALL, end='\r')
    if not bool(value):
        value = default_value
    return value


def print_used_value(description: str, value: str):
    print(f'{description}: {Fore.GREEN}{value}{Style.RESET_ALL}')


def is_ip(address: str) -> bool:
    return address.replace('.', '').isnumeric()


def write_file(name: str, content: any):
    f = open(name, "w")
    f.write(content)
    f.close()
