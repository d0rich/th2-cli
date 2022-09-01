from kubernetes.utils import create_from_yaml
from th2_cli.utils import get_yaml_config
from th2_cli.utils.kubernetes import connect, create_namespace_object
from th2_cli.utils.infra import install_flannel, create_namespace


def install_1_5():
    print('Connecting to the cluster...')
    k8s_client, k8s_core = connect()
    print("Preparing Kubernetes cluster...")
    # Install flannel
    install_flannel(k8s_client)
    # Create namespaces
    create_namespace(k8s_core, 'monitoring')
    create_namespace(k8s_core, 'service')
    #
