from kubernetes.client import ApiClient, CoreV1Api, V1Namespace
from kubernetes import client, config
from typing import Tuple


def connect() -> Tuple[ApiClient, CoreV1Api]:
    config.load_kube_config()
    k8s_client = client.ApiClient()
    k8s_core = client.CoreV1Api()
    return k8s_client, k8s_core


def create_namespace_object(name: str) -> V1Namespace:
    return V1Namespace(metadata=client.V1ObjectMeta(name=name))
