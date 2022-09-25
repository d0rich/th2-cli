from th2_cli.utils import read_value, is_ip, write_file, print_info, print_used_value
from th2_cli.utils.kubernetes import connect, get_cluster_host, create_secret
from th2_cli.utils.cassandra import choose_datacenter
from th2_cli.utils.crypto import generate_ssh_keys
from th2_cli.utils.helm.charts_installer import ChartsInstaller
from th2_cli.utils.infra import install_flannel, create_namespace, choose_node, \
    apply_yaml, pv_folders_warning
from simple_term_menu import TerminalMenu
from th2_cli.templates.install import InstallTemplates

TH2_VERSION = '1.5.4'


def install():
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
    apply_yaml(k8s_client, InstallTemplates.pvs(node_name=node), 'pvs.yaml')
    apply_yaml(k8s_client, InstallTemplates.pvcs(), 'pvcs.yaml')
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
    charts_installer = ChartsInstaller(namespace='monitoring', th2_version=TH2_VERSION)
    charts_installer.add_helm_release('prometheus-community', 'kube-prometheus-stack',
                                      'https://prometheus-community.github.io/helm-charts', '15.0.0',
                                      InstallTemplates.prometheus_operator_values(hosts=cluster_hostname))
    charts_installer.add_helm_release('kubernetes-dashboard', 'kubernetes-dashboard',
                                      'https://kubernetes.github.io/dashboard/', '5.9.0',
                                      InstallTemplates.dashboard_values(hosts=cluster_hostname))
    charts_installer.add_helm_release('grafana', 'loki-stack',
                                      'https://grafana.github.io/helm-charts', '0.40.1',
                                      InstallTemplates.loki_values())
    charts_installer.install_charts()
    print_info('Deploying service infrastructure...')
    charts_installer = ChartsInstaller(namespace='service', th2_version=TH2_VERSION)
    charts_installer.add_helm_release('fluxcd', 'helm-operator',
                                      'https://charts.fluxcd.io', '1.2.0',
                                      InstallTemplates.helm_operator_values())
    charts_installer.add_helm_release('ingress-nginx', 'ingress-nginx',
                                      'https://kubernetes.github.io/ingress-nginx', '3.31.0',
                                      InstallTemplates.ingress_values())
    charts_installer.add_helm_release('th2', 'th2',
                                      'https://th2-net.github.io', '1.5.4',
                                      {
                                          **InstallTemplates.service_values(schema_link=schema_link,
                                                                            pat_token=token or '',
                                                                            cluster_host=cluster_hostname or cluster_host,
                                                                            cassandra_host=cassandra_host,
                                                                            cassandra_datacenter=cassandra_dc),
                                          **InstallTemplates.secrets()
                                      })
    charts_installer.install_charts()
    print_info(f'th2 {TH2_VERSION} is installed')




