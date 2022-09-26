from th2_cli.utils.infra import pre_delete_warning, get_infra_mgr_config, delete_namespace
from th2_cli.utils import read_value, print_info, print_used_value
from th2_cli.utils.kubernetes import connect, get_namespaces


def delete():
    pre_delete_warning()
    print_info('Connecting to the cluster...')
    k8s_client, k8s_core = connect()
    prefix = get_infra_mgr_config(k8s_core)['kubernetes']['namespacePrefix']
    th2_namespaces = filter(lambda ns: ns.startswith(prefix), get_namespaces(k8s_core))
    print_info('Deleting "monitoring" namespace...')
    delete_namespace(k8s_core, 'monitoring')
    print_info('Deleting "service" namespace...')
    delete_namespace(k8s_core, 'service')
    print_info('Deleting th2 namespaces...')
    for ns in th2_namespaces:
        print_info(f'Deleting {ns} namespace...')
        delete_namespace(k8s_core, ns)
    print_info('th2 is deleted from your Kubernetes cluster')
