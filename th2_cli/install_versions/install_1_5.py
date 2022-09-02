from kubernetes.utils import create_from_yaml
from th2_cli.utils import read_value, is_ip
from th2_cli.utils.kubernetes import connect, get_namespaces, get_nodes, get_cluster_host
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
    cluster_host = get_cluster_host(k8s_client)
    if is_ip(cluster_host):
        cluster_hostname = read_value('Enter Kubernetes cluster hostname, if it exist.', 'hostname')
    else:
        cluster_hostname = cluster_host
    cassandra_host = read_value('Enter hostname of Cassandra.',
                                'host', '127.0.0.1')
    cassandra_dc = read_value('Enter Cassandra datacenter name.', 'datacenter', 'datacenter1')
    schema_link = read_value('Enter link to your infra-schema')




