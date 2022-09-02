from kubernetes.client import ApiClient, CoreV1Api, V1Namespace
from kubernetes.utils import create_from_yaml
from simple_term_menu import TerminalMenu
from typing import Dict
import yaml

from th2_cli.utils.kubernetes import create_namespace_object, get_nodes
from th2_cli.utils import get_yaml_config, get_file


def create_namespace(k8s_core: CoreV1Api, name: str):
    try:
        k8s_core.create_namespace(create_namespace_object(name))
        print(f'"{name}" namespace created')
    except:
        print(f'"{name}" namespace already exist')


def install_flannel(k8s_client: ApiClient):
    try:
        flannel_manifest = get_yaml_config(
            "https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml")
        create_from_yaml(k8s_client=k8s_client, yaml_objects=flannel_manifest)
        print('flannel-cni is installed')
    except:
        print("Error while installing flannel. It might already exist")


def choose_node(k8s_core: CoreV1Api) -> str:
    nodes = get_nodes(k8s_core)
    terminal_menu = TerminalMenu(nodes, title='Kubernetes nodes:')
    node_index = terminal_menu.show()
    chosen_node = nodes[node_index]
    return chosen_node


def change_and_apply_config_template(k8s_client: ApiClient, version: str, file_path: str, inserts: Dict[str, str] = {}):
    raw_template = get_file(f'assets/config-templates/{version}/{file_path}')
    new_config = raw_template
    for insert in inserts:
        new_config = new_config.replace(f'<{insert}>', inserts[insert])
    yaml_obj = yaml.safe_load_all(new_config)
    try:
        create_from_yaml(k8s_client=k8s_client, yaml_objects=yaml_obj)
    except:
        print(f'Error while applying "{file_path}"')