from th2_cli.utils.kubernetes import connect, get_namespaces, get_namespace_status


def status():
    k8s_client, k8s_core = connect()
    namespaces = get_namespaces(k8s_core)
    for ns in filter(lambda ns: ns in ['monitoring', 'service'] or 'th2' in ns, namespaces):
        print(f'{ns} - {get_namespace_status(k8s_core, ns)}')
