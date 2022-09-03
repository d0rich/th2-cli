from kubernetes.utils import create_from_yaml
from th2_cli.utils import read_value, is_ip
from th2_cli.utils.kubernetes import connect, get_namespaces, get_nodes, get_cluster_host
from th2_cli.utils.helm.charts_installer import ChartsInstaller
from th2_cli.utils.infra import install_flannel, create_namespace, choose_node, \
    change_and_apply_config_template, load_and_change_config_template
import yaml

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
        cluster_hostname = ''
    cassandra_host = read_value('Enter hostname of Cassandra.',
                                'host', '127.0.0.1')
    cassandra_dc = read_value('Enter Cassandra datacenter name.', 'datacenter', 'datacenter1')
    schema_link = read_value('Enter link to your infra-schema', 'link')
    token = read_value('Enter PAT for your infra-schema', 'PAT')
    charts_installer = ChartsInstaller(namespace='monitoring', th2_version=VERSION)
    charts_installer.add_helm_release('prometheus-community', 'kube-prometheus-stack',
                                      'https://prometheus-community.github.io/helm-charts', '15.0.0',
                                      yaml.safe_load(
                                          load_and_change_config_template(VERSION, 'prometheus-operator.values.yaml',
                                                                          {'hosts': cluster_hostname})
                                      ))
    charts_installer.add_helm_release('kubernetes-dashboard', 'kubernetes-dashboard',
                                      'https://kubernetes.github.io/dashboard/', '5.9.0',
                                      yaml.safe_load(
                                          load_and_change_config_template(VERSION, 'dashboard.values.yaml',
                                                                          {'hosts': cluster_hostname})
                                      ))
    charts_installer.add_helm_release('grafana', 'loki-stack',
                                      'https://grafana.github.io/helm-charts', '0.40.1',
                                      yaml.safe_load(
                                          load_and_change_config_template(VERSION, 'loki.values.yaml')
                                      ))
    charts_installer.install_charts()
    charts_installer = ChartsInstaller(namespace='service', th2_version=VERSION)
    charts_installer.add_helm_release('fluxcd', 'helm-operator',
                                      'https://charts.fluxcd.io', '1.2.0',
                                      yaml.safe_load(
                                          load_and_change_config_template(VERSION, 'helm-operator.values.yaml')
                                      ))
    charts_installer.add_helm_release('ingress-nginx', 'ingress-nginx',
                                      'https://kubernetes.github.io/ingress-nginx', '3.31.0',
                                      yaml.safe_load(
                                          load_and_change_config_template(VERSION, 'ingress.values.yaml')
                                      ))
    charts_installer.add_helm_release('th2', 'th2',
                                      'https://th2-net.github.io', '1.5.4',
                                      {
                                          **yaml.safe_load(
                                              load_and_change_config_template(VERSION, 'service.values.yaml', {
                                                  'repository': schema_link,
                                                  'host': cluster_hostname or cluster_host,
                                                  'cassandra-host': cassandra_host,
                                                  'cassandra-dc': cassandra_dc,
                                                  'username': token,
                                                  'password': token
                                              })
                                          ),
                                          **yaml.safe_load(
                                              load_and_change_config_template(VERSION, 'secrets.yaml')
                                          )
                                      })

    charts_installer.install_charts()




