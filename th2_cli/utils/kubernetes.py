from kubernetes.client import ApiClient, CoreV1Api, V1Namespace
from kubernetes import client, config
from typing import Tuple, List


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

