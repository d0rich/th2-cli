from kubernetes.utils import create_from_yaml
from th2_cli.utils import get_yaml_config
from th2_cli.utils.kubernetes import connect, create_namespace_object


def install_1_5():
    print('Connecting to the cluster...')
    k8s_client, k8s_core = connect()
    print("Preparing Kubernetes cluster...")
    # Install flannel
    try:
        flannel_manifest = get_yaml_config(
            "https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml")
        create_from_yaml(k8s_client=k8s_client, yaml_objects=flannel_manifest)
        print('flannel-cni is installed')
    except:
        print("Error while installing flannel. It might exist")
    # Create namespaces
    try:
        k8s_core.create_namespace(create_namespace_object('monitoring'))
        print('monitoring namespace created')
    except:
        print('monitoring namespace already exist')
    try:
        k8s_core.create_namespace(create_namespace_object('service'))
        print('service namespace created')
    except:
        print('service namespace already exist')
    #
