from kubernetes.utils import create_from_yaml
from th2_cli.utils import get_yaml_config
from th2_cli.utils.kubernetes import connect, get_namespaces, get_nodes
from th2_cli.utils.infra import install_flannel, create_namespace, choose_node, change_and_apply_config_template

VERSION = '1.5'


def install_1_5():
    print('Connecting to the cluster...')
    k8s_client, k8s_core = connect()
    print("Preparing Kubernetes cluster...")
    # Install flannel
    install_flannel(k8s_client)
    # Create namespaces
    create_namespace(k8s_core, 'monitoring')
    create_namespace(k8s_core, 'service')
    # Apply PV's
    # TODO: add warning about created folders
    print('Please choose node for storing PersistentVolumes')
    node = choose_node(k8s_core)
    print(f'PersistentVolumes will be stored on "{node}" node')
    print('Creating PV\'s and PVC\'s')
    change_and_apply_config_template(k8s_client, VERSION, 'pvs.yaml', {'node-name': node})
    change_and_apply_config_template(k8s_client, VERSION, 'pvcs.yaml')
    print('PV\'s and PVC\'s are created')

