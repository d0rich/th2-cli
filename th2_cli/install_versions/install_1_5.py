from kubernetes import client, config
from kubernetes.utils import create_from_yaml
from th2_cli.utils import get_file

config.load_kube_config()
k8s_client = client.ApiClient()
k8s_core = client.CoreV1Api()


def install_1_5():
    print("Preparing Kubernetes cluster...")
    flannel_manifest = get_file(
        "https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml")
    create_from_yaml(k8s_client=k8s_client, yaml_file=flannel_manifest)
    k8s_core.create_namespace(client.V1Namespace(metadata=client.V1ObjectMeta(name="monitoring")))
    k8s_core.create_namespace(client.V1Namespace(metadata=client.V1ObjectMeta(name="service")))
