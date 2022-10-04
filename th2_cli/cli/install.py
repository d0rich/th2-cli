import deepmerge

from th2_cli.utils import read_value, is_ip, write_file, print_info, print_used_value, yes_no_input, check_file, \
    enter_to_continue
from th2_cli.utils.kubernetes import connect, get_cluster_host, create_secret
from th2_cli.utils.cassandra import choose_datacenter
from th2_cli.utils.crypto import generate_ssh_keys
from th2_cli.utils.helm.charts_installer import ChartsInstaller
from th2_cli.utils.infra import install_flannel, create_namespace, choose_node, \
    apply_yaml, pv_folders_warning, preinstall_warning
from th2_cli.utils.install_config import InstallConfig
from simple_term_menu import TerminalMenu
from th2_cli.templates.install import InstallTemplates

TH2_VERSION = '1.7.3'


def install():
    preinstall_warning()
    print_info('Connecting to the cluster...')
    k8s_client, k8s_core = connect()
    if check_file('th2-cli-install-config.yaml'):
        if yes_no_input('th2 installation config is detected. Do you want to load configuration?', True):
            install_config = InstallConfig.from_yaml_file('th2-cli-install-config.yaml')
        else:
            install_config = InstallConfig()
    else:
        install_config = InstallConfig()
    print_info("Preparing Kubernetes cluster...")
    # Install flannel
    install_flannel(k8s_client)
    # Create namespaces
    create_namespace(k8s_core, 'monitoring')
    create_namespace(k8s_core, 'service')
    # Apply PV's
    print('Please choose node for storing PersistentVolumes')
    if install_config.kubernetes.pvs_node_is_default():
        install_config.kubernetes.pvs_node = choose_node(k8s_core)
    print_used_value('Node for PersistentVolumes storage', install_config.kubernetes.pvs_node)
    pv_folders_warning()
    print_info('Creating PV\'s and PVC\'s...')
    apply_yaml(k8s_client, InstallTemplates.pvs(node_name=install_config.kubernetes.pvs_node), 'pvs.yaml')
    apply_yaml(k8s_client, InstallTemplates.pvcs(), 'pvcs.yaml')
    # Get information about Kubernetes cluster
    if install_config.kubernetes.host_is_default():
        install_config.kubernetes.host = get_cluster_host(k8s_client)
    print_used_value('Cluster host', install_config.kubernetes.host)
    if is_ip(install_config.kubernetes.host):
        install_config.kubernetes.host = read_value('Enter Kubernetes cluster hostname, if it exist.', 'hostname') \
                                         or install_config.kubernetes.host
        print_used_value('Cluster hostname', install_config.kubernetes.hostname or '')
    # Get information about Cassandra database
    if install_config.cassandra.host_is_default():
        install_config.cassandra.host = read_value('Enter hostname of Cassandra to access it from the '
                                                   'Kubernetes cluster', 'host', '127.0.0.1')
    print_used_value('Cassandra host', install_config.cassandra.host)
    if install_config.cassandra.datacenter_is_default():
        dc_input_index = TerminalMenu(
            [
                'Enter datacenter manually',
                'Connect to Cassandra and choose available datacenter (Admin credentials required)'
            ],
            title='How do you want to specify Cassandra datacenter?'
        ).show()
        if dc_input_index == 0:
            install_config.cassandra.datacenter = read_value('Enter Cassandra datacenter name.', 'datacenter',
                                                             'datacenter1')
        else:
            install_config.cassandra.datacenter = choose_datacenter(install_config.cassandra.host)
    print_used_value('Cassandra datacenter', install_config.cassandra.datacenter)
    # Get information about infra-schema
    if install_config.infra_mgr.git.repository_is_default():
        install_config.infra_mgr.git.repository = read_value('Enter link to your infra-schema', 'link')
    print_used_value('th2-infra-schema link', install_config.infra_mgr.git.repository)
    if install_config.infra_mgr.git.repository.startswith('https://'):
        if install_config.infra_mgr.git.http_auth_username_is_default() or install_config.infra_mgr.git.http_auth_password_is_default():
            print_info('th2 will be authenticated in git by Personal Access Token (PAT)')
            token = read_value('Enter PAT for your infra-schema', 'PAT')
            install_config.infra_mgr.git.http_auth_username = token
            install_config.infra_mgr.git.http_auth_password = token
        print_used_value('Personal Access Token', install_config.infra_mgr.git.http_auth_username)
        create_secret(k8s_core, 'infra-mgr', namespace='service', string_data={'infra-mgr': 'infra-mgr'})
    else:
        print_info('th2 will be authenticated in git by SSH key')
        private_key, public_key = generate_ssh_keys()
        write_file('infra-mgr-rsa.key', private_key)
        write_file('infra-mgr-rsa.key.pub', public_key)
        create_secret(k8s_core, 'infra-mgr', namespace='service', string_data={'infra-mgr': private_key})
    if check_file('secrets.yaml'):
        if yes_no_input('"secrets.yaml" file is detected. Would you like to rewrite it with template?'):
            InstallTemplates.create_secrets_template()
            print_info('"secrets.yaml" template is created.')
    else:
        InstallTemplates.create_secrets_template()
        print_info('"secrets.yaml" template is created.')
    print('Fill "secrets.yaml" with relevant credentials')
    enter_to_continue()
    # Deploy infrastructure
    print_info('Deploying monitoring infrastructure...')
    charts_installer = ChartsInstaller(namespace='monitoring')
    charts_installer.add_helm_release('prometheus-community', 'kube-prometheus-stack',
                                      'https://prometheus-community.github.io/helm-charts', '15.0.0',
                                      InstallTemplates.prometheus_operator_values(
                                          hosts=install_config.kubernetes.hostname))
    charts_installer.add_helm_release('grafana', 'loki-stack',
                                      'https://grafana.github.io/helm-charts', '2.4.1',
                                      InstallTemplates.loki_values())
    charts_installer.install_charts()
    print_info('Deploying service infrastructure...')
    charts_installer = ChartsInstaller(namespace='service')
    charts_installer.add_helm_release('ingress-nginx', 'ingress-nginx',
                                      'https://kubernetes.github.io/ingress-nginx', '3.31.0',
                                      InstallTemplates.ingress_values())
    th2_values: dict = deepmerge.always_merger.merge(
        InstallTemplates.service_values(
                                              schema_link=install_config.infra_mgr.git.repository,
                                              git_username=install_config.infra_mgr.git.http_auth_username,
                                              git_password=install_config.infra_mgr.git.http_auth_password,
                                              cluster_host=install_config.kubernetes.host,
                                              cluster_hostname=install_config.kubernetes.hostname,
                                              cassandra_host=install_config.cassandra.host,
                                              cassandra_datacenter=install_config.cassandra.datacenter),
        InstallTemplates.get_secrets())
    charts_installer.add_helm_release('th2', 'th2',
                                      'https://th2-net.github.io', '1.7.3',
                                      th2_values)
    charts_installer.install_charts()
    print_info(f'th2 {TH2_VERSION} is installed')
    if yes_no_input('Would you like to save th2 config in the current directory?', True):
        write_file('th2-cli-install-config.yaml', install_config.to_yaml())
