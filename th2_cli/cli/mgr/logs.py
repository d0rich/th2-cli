from th2_cli.utils.kubernetes import get_pods, get_pod_logs, connect


def logs():
    k8s_client, k8s_core = connect()
    pods = get_pods(k8s_core, 'service')
    mgr_pod = next((pod for pod in pods if pod.startswith('infra-mgr')), None)
    print(get_pod_logs(k8s_core, mgr_pod, 'service'))
