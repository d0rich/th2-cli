from kubernetes import client, config
from kubernetes.utils import create_from_yaml
from th2_cli.utils import get_file
import yaml

config.load_kube_config()
k8s_client = client.ApiClient()
k8s_core = client.CoreV1Api()


def install_1_5():
    print("Preparing Kubernetes cluster...")
    # Install flannel
    try:
        flannel_manifest = get_file(
            "https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml")
        create_from_yaml(k8s_client=k8s_client, yaml_objects=yaml.safe_load_all(flannel_manifest))
        print('flannel-cni is installed')
    except:
        print("Error while installing flannel. It might exist")
    # Create namespaces
    try:
        k8s_core.create_namespace(client.V1Namespace(metadata=client.V1ObjectMeta(name="monitoring")))
        print('monitoring namespace created')
    except:
        print('monitoring namespace already exist')
    try:
        k8s_core.create_namespace(client.V1Namespace(metadata=client.V1ObjectMeta(name="service")))
        print('service namespace created')
    except:
        print('service namespace already exist')
