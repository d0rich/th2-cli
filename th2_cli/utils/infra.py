from kubernetes.client import ApiClient, CoreV1Api, V1Namespace
from kubernetes.utils import create_from_yaml
from colorama import Fore, Style, Back
from simple_term_menu import TerminalMenu
from typing import Dict
import yaml

from th2_cli.utils.kubernetes import create_namespace_object, get_nodes
from th2_cli.utils import get_yaml_config, get_file, print_error


def pv_folders_warning():
    print(
        f'{Fore.YELLOW}Be sure that you have created folders on the chosen node:\n mkdir /opt/grafana /opt/prometheus /opt/loki /opt/rabbitmq{Style.RESET_ALL}')
    input(f'Press {Back.YELLOW}Enter{Style.RESET_ALL} to continue')


def create_namespace(k8s_core: CoreV1Api, name: str):
    try:
        k8s_core.create_namespace(create_namespace_object(name))
        print(f'"{name}" namespace created')
    except:
        print_error(f'"{name}" namespace already exist')


def install_flannel(k8s_client: ApiClient):
    try:
        flannel_manifest = get_yaml_config(
            "https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml")
        create_from_yaml(k8s_client=k8s_client, yaml_objects=flannel_manifest)
        print(f'flannel-cni is installed')
    except:
        print_error(f"Error while installing flannel. It might already exist")


def choose_node(k8s_core: CoreV1Api) -> str:
    nodes = get_nodes(k8s_core)
    terminal_menu = TerminalMenu(nodes, title='Kubernetes nodes:')
    node_index = terminal_menu.show()
    chosen_node = nodes[node_index]
    return chosen_node


def load_and_change_config_template(version: str, file_path: str, inserts: Dict[str, str] = {}) -> str:
    raw_template = get_file(f'assets/config-templates/{version}/{file_path}')
    new_config = raw_template
    for insert in inserts:
        new_config = new_config.replace(f'<{insert}>', inserts[insert])
    return new_config


def change_and_apply_config_template(k8s_client: ApiClient, version: str, file_path: str, inserts: Dict[str, str] = {}):
    config = load_and_change_config_template(version, file_path, inserts)
    yaml_obj = yaml.safe_load_all(config)
    try:
        create_from_yaml(k8s_client=k8s_client, yaml_objects=yaml_obj)
    except:
        print_error(f'Error while applying "{file_path}"')
