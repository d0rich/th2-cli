import yaml
from typing import Iterator
from th2_cli.utils import get_file, write_file

from th2_cli.templates.install.values.ingress import yaml as ingress_values_yaml
from th2_cli.templates.install.values.loki import yaml as loki_values_yaml
from th2_cli.templates.install.values.prometheus_operator import yaml as prometheus_operator_values_yaml
from th2_cli.templates.install.values.secrets import yaml as secrets_yaml
from th2_cli.templates.install.values.service import yaml as service_values_yaml
from th2_cli.templates.install.pvs import yaml as pvs_yaml
from th2_cli.templates.install.pvcs import yaml as pvcs_yaml


class InstallTemplates:

    @staticmethod
    def ingress_values() -> dict:
        changed_template = ingress_values_yaml
        return yaml.safe_load(changed_template)

    @staticmethod
    def loki_values() -> dict:
        changed_template = loki_values_yaml
        return yaml.safe_load(changed_template)

    @staticmethod
    def prometheus_operator_values(hosts: str = '') -> dict:
        changed_template = prometheus_operator_values_yaml \
            .replace('<hosts>', hosts)
        return yaml.safe_load(changed_template)

    @staticmethod
    def create_secrets_template():
        write_file('secrets.yaml', secrets_yaml)

    @staticmethod
    def get_secrets() -> dict:
        changed_template = get_file('secrets.yaml')
        return yaml.safe_load(changed_template)

    @staticmethod
    def service_values(schema_link: str, git_username: str = '', git_password: str = '',
                       cluster_host: str = '', cluster_hostname: str = '',
                       cassandra_host: str = '127.0.0.1', cassandra_datacenter: str = 'datacenter1') -> dict:
        changed_template = service_values_yaml \
            .replace('<repository>', schema_link) \
            .replace('<username>', git_username) \
            .replace('<password>', git_password) \
            .replace('<host>', cluster_host) \
            .replace('<hostname>', cluster_hostname) \
            .replace('<cassandra-host>', cassandra_host) \
            .replace('<cassandra-dc>', cassandra_datacenter)
        return yaml.safe_load(changed_template)

    @staticmethod
    def pvs(node_name: str) -> Iterator[dict]:
        changed_template = pvs_yaml.replace('<node-name>', node_name)
        return yaml.safe_load_all(changed_template)

    @staticmethod
    def pvcs() -> Iterator[dict]:
        changed_template = pvcs_yaml
        return yaml.safe_load_all(changed_template)
