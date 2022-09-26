from th2_cli.utils.infra import pre_delete_warning, get_infra_mgr_config
from th2_cli.utils import read_value, print_info, print_used_value
from th2_cli.utils.kubernetes import connect


def delete():
    pre_delete_warning()
    print_info('Connecting to the cluster...')
    k8s_client, k8s_core = connect()
    prefix = get_infra_mgr_config(k8s_core)['kubernetes']['namespacePrefix']
    print(prefix)

