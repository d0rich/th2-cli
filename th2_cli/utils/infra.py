from kubernetes.client import ApiClient, CoreV1Api
from kubernetes.utils import create_from_yaml
from colorama import Fore, Style, Back
from simple_term_menu import TerminalMenu
from typing import Iterator
import yaml

from th2_cli.utils.kubernetes import create_namespace_object, get_nodes
from th2_cli.utils import get_yaml_config, print_error, enter_to_continue


def preinstall_warning():
    print(f'{Fore.YELLOW}Before th2 installation you should fulfill following prerequisites:')
    print(
        f'  1. You should have {Fore.CYAN}Kubernetes cluster{Fore.YELLOW} deployed {Fore.RED}(v1.19 - 1.20){Fore.YELLOW};')
    print(f'    1.1. You should have {Fore.CYAN}kubectl{Fore.YELLOW} installed and configured with {Fore.RED}k8s admin '
          f'profile{Fore.YELLOW};')
    print(
        f'  2. You should have {Fore.CYAN}Cassandra database{Fore.YELLOW} deployed {Fore.RED}(v3.11.6+){Fore.YELLOW}.{Style.RESET_ALL}')
    proceed = input(f'Proceed to th2 installation ({Fore.YELLOW}y/N{Style.RESET_ALL}): ')
    if proceed.lower() != 'y':
        print(f'{Fore.YELLOW}Cancelling installation...{Style.RESET_ALL}')
        exit(1)


def pre_delete_warning():
    print(f'{Fore.YELLOW}For th2 deletion you should have {Fore.CYAN}kubectl{Fore.YELLOW} installed and configured with'
          f' {Fore.RED}k8s admin profile{Style.RESET_ALL}')
    proceed = input(f'Proceed to th2 deletion ({Fore.YELLOW}y/N{Style.RESET_ALL}): ')
    if proceed.lower() != 'y':
        print(f'{Fore.YELLOW}Cancelling deletion...{Style.RESET_ALL}')
        exit(1)


def pv_folders_warning():
    print(f'{Fore.YELLOW}Be sure that you have created folders on the chosen node:')
    print(f'{Style.BRIGHT}mkdir /opt/grafana /opt/prometheus /opt/loki /opt/rabbitmq{Style.RESET_ALL}')
    enter_to_continue()


def create_namespace(k8s_core: CoreV1Api, name: str):
    try:
        k8s_core.create_namespace(create_namespace_object(name))
        print(f'"{name}" namespace created')
    except:
        print_error(f'"{name}" namespace already exist')


def delete_namespace(k8s_core: CoreV1Api, name: str):
    try:
        k8s_core.delete_namespace(name=name)
    except:
        print_error(f'Unable to delete "{name}" namespace')


def delete_pv(k8s_core: CoreV1Api, name: str):
    try:
        k8s_core.delete_persistent_volume(name=name)
    except:
        print_error(f'Unable to delete "{name}" PersistentVolume')


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


def apply_yaml(k8s_client: ApiClient, yaml_obj: Iterator[dict], file_name: str = 'undefined'):
    try:
        create_from_yaml(k8s_client=k8s_client, yaml_objects=yaml_obj)
    except:
        print_error(f'Error while applying "{file_name}"')


def get_infra_mgr_config(k8s_core: CoreV1Api) -> dict:
    try:
        config_map = k8s_core.read_namespaced_config_map('infra-mgr', 'service')
        config = yaml.safe_load(config_map.data['config.yml'])
        return config
    except:
        print_error(f'Error accessing th2-infra-mgr config map')
