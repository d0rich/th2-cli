from th2_cli.utils import read_value, is_ip, write_file, print_info, print_used_value
from th2_cli.utils.kubernetes import connect, get_cluster_host, create_secret
from th2_cli.utils.cassandra import choose_datacenter
from th2_cli.utils.crypto import generate_ssh_keys
from th2_cli.utils.helm.charts_installer import ChartsInstaller
from th2_cli.utils.infra import install_flannel, create_namespace, choose_node, \
    change_and_apply_config_template, load_and_change_config_template, pv_folders_warning
import yaml
from simple_term_menu import TerminalMenu

VERSION = '1.5'


def install_1_5():
    print_info('Connecting to the cluster...')
    k8s_client, k8s_core = connect()
    print_info("Preparing Kubernetes cluster...")
    # Install flannel
    install_flannel(k8s_client)
    # Create namespaces
    create_namespace(k8s_core, 'monitoring')
    create_namespace(k8s_core, 'service')
    # Apply PV's
    print('Please choose node for storing PersistentVolumes')
    node = choose_node(k8s_core)
    print_used_value('Node for PersistentVolumes storage', node)
    pv_folders_warning()
    print_info('Creating PV\'s and PVC\'s...')
    change_and_apply_config_template(k8s_client, VERSION, 'pvs.yaml', {'node-name': node})
    change_and_apply_config_template(k8s_client, VERSION, 'pvcs.yaml')
    # Get information about Kubernetes cluster
    cluster_host = get_cluster_host(k8s_client)
    print_used_value('Cluster host', cluster_host)
    if is_ip(cluster_host):
        cluster_hostname = read_value('Enter Kubernetes cluster hostname, if it exist.', 'hostname')
        print_used_value('Cluster hostname', cluster_hostname)
    else:
        cluster_hostname = ''
    # Get information about Cassandra database
    cassandra_host = read_value('Enter hostname of Cassandra to access it from the Kubernetes cluster', 'host', '127.0.0.1')
    print_used_value('Cassandra host', cassandra_host)
    dc_input_index = TerminalMenu(
        [
            'Enter datacenter manually',
            'Connect to Cassandra and choose available datacenter (Admin credentials required)'
        ],
        title='How do you want to specify Cassandra datacenter?'
    ).show()
    if dc_input_index == 0:
        cassandra_dc = read_value('Enter Cassandra datacenter name.', 'datacenter', 'datacenter1')
    else:
        cassandra_dc = choose_datacenter(cassandra_host)
    print_used_value('Cassandra datacenter', cassandra_dc)
    # Get information about infra-schema
    schema_link = read_value('Enter link to your infra-schema', 'link')
    print_used_value('th2-infra-schema link', schema_link)
    if schema_link.startswith('https://'):
        print_info('th2 will be authenticated in git by Personal Access Token (PAT)')
        token = read_value('Enter PAT for your infra-schema', 'PAT')
        print_used_value('Personal Access Token', token)
        create_secret(k8s_core, 'infra-mgr', namespace='service', string_data={'infra-mgr': 'infra-mgr'})
    else:
        token = None
        print_info('th2 will be authenticated in git by SSH key')
        private_key, public_key = generate_ssh_keys()
        write_file('infra-mgr-rsa.key', private_key)
        write_file('infra-mgr-rsa.key.pub', public_key)
        create_secret(k8s_core, 'infra-mgr', namespace='service', string_data={'infra-mgr': private_key})
    # Deploy infrastructure
    print_info('Deploying monitoring infrastructure...')
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
    print_info('Deploying service infrastructure...')
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
                                                  'username': token or '',
                                                  'password': token or ''
                                              })
                                          ),
                                          **yaml.safe_load(
                                              load_and_change_config_template(VERSION, 'secrets.yaml')
                                          )
                                      })
    charts_installer.install_charts()
    print_info(f'th2 {VERSION} is installed')




