from kubernetes.client import ApiClient, CoreV1Api, V1Namespace
from kubernetes.utils import create_from_yaml
from th2_cli.utils.kubernetes import create_namespace_object
from th2_cli.utils import get_yaml_config


def create_namespace(k8s_core: CoreV1Api, name: str):
    try:
        k8s_core.create_namespace(create_namespace_object(name))
        print(f'{name} namespace created')
    except:
        print(f'{name} namespace already exist')


def install_flannel(k8s_client: ApiClient):
    try:
        flannel_manifest = get_yaml_config(
            "https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml")
        create_from_yaml(k8s_client=k8s_client, yaml_objects=flannel_manifest)
        print('flannel-cni is installed')
    except:
        print("Error while installing flannel. It might already exist")