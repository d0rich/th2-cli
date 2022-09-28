from th2_cli.utils.kubernetes import get_pods, get_pod_status, connect
from th2_cli.utils import print_error


def status():
    k8s_client, k8s_core = connect()
    pods = get_pods(k8s_core, 'service')
    mgr_pod = next((pod for pod in pods if pod.startswith('infra-mgr')), None)
    if not mgr_pod:
        print_error('infra-mgr does not exist')
    else:
        print(get_pod_status(k8s_core, mgr_pod, 'service'))
