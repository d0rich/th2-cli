from dataclasses import dataclass
from dataclass_wizard import YAMLWizard
from th2_cli.utils import is_ip


@dataclass
class InstallConfig(YAMLWizard):
    @dataclass
    class KubernetesConfigSection:
        pvs_node: str = ''
        host: str = ''

        def hostname(self) -> str:
            if is_ip(self.host):
                return ''
            return self.host

    @dataclass
    class CassandraConfigSection:
        host: str = '127.0.0.1'
        datacenter: str = 'datacenter1'

    @dataclass
    class InfraMgrConfigSection:
        @dataclass
        class GitSection:
            repository: str = ''
            http_auth_username: str = ''
            http_auth_password: str = ''

        git: GitSection = GitSection()

    kubernetes: KubernetesConfigSection = KubernetesConfigSection()
    cassandra: CassandraConfigSection = CassandraConfigSection()
    infra_mgr: InfraMgrConfigSection = InfraMgrConfigSection()
