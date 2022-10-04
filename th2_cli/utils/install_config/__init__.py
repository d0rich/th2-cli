from dataclasses import dataclass
from dataclass_wizard import YAMLWizard
from th2_cli.utils.install_config.kubernetes import KubernetesConfigSection
from th2_cli.utils.install_config.cassandra import CassandraConfigSection
from th2_cli.utils.install_config.infra_mgr import InfraMgrConfigSection


@dataclass
class InstallConfig(YAMLWizard):
    kubernetes: KubernetesConfigSection = KubernetesConfigSection()
    cassandra: CassandraConfigSection = CassandraConfigSection()
    infra_mgr: InfraMgrConfigSection = InfraMgrConfigSection()
