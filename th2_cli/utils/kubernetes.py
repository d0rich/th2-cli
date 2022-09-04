from kubernetes.client import ApiClient, CoreV1Api, V1Namespace
from kubernetes import client, config
from urllib.parse import urlparse
from typing import Tuple, List
from th2_cli.utils import print_error


def connect() -> Tuple[ApiClient, CoreV1Api]:
    config.load_kube_config()
    k8s_client = client.ApiClient()
    k8s_core = client.CoreV1Api()
    return k8s_client, k8s_core


def create_namespace_object(name: str) -> V1Namespace:
    return V1Namespace(metadata=client.V1ObjectMeta(name=name))


def get_namespaces(k8s_core: CoreV1Api) -> List[str]:
    namespaces = list(
        map(lambda item: item.metadata.name, k8s_core.list_namespace().items)
    )
    return namespaces


def get_nodes(k8s_core: CoreV1Api) -> List[str]:
    nodes = list(
        map(lambda item: item.metadata.name, k8s_core.list_node().items)
    )
    return nodes


def get_cluster_host(k8s_client: ApiClient) -> str:
    url = k8s_client.configuration.host
    return urlparse(url).netloc.split(':')[0]


def create_secret(k8s_core: CoreV1Api, name: str, data: dict = None, string_data: dict = None,
                  namespace: str = 'service'):
    try:
        secret = client.V1Secret(
            metadata=client.V1ObjectMeta(name=name),
            data=data,
            string_data=string_data
        )
        k8s_core.create_namespaced_secret(namespace=namespace,
                                          body=secret)
    except:
        print_error(f'Failed to create "{name}" secret')

