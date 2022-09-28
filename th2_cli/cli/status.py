from th2_cli.utils.kubernetes import connect, get_namespaces, get_namespace_status
from th2_cli.utils import print_error


def status():
    k8s_client, k8s_core = connect()
    namespaces = get_namespaces(k8s_core)
    namespaces = list(filter(lambda ns: ns in ['monitoring', 'service'] or 'th2' in ns, namespaces))
    if len(namespaces):
        for ns in namespaces:
            print(f'{ns} - {get_namespace_status(k8s_core, ns)}')
    else:
        print_error('th2 is not installed')
