from kubernetes.client import ApiClient, CoreV1Api, V1Namespace
from kubernetes.utils import create_from_yaml
from simple_term_menu import TerminalMenu
from th2_cli.utils.kubernetes import create_namespace_object, get_nodes
from th2_cli.utils import get_yaml_config


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
    print('Please choose node for storing PersistentVolumes')
    node_index = terminal_menu.show()
    chosen_node = nodes[node_index]
    print(f'PersistentVolumes will be stored on "{chosen_node}" node')
    return chosen_node
