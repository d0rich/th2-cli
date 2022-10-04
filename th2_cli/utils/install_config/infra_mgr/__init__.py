from dataclasses import dataclass
from th2_cli.utils.install_config.infra_mgr.git import GitSection


@dataclass
class InfraMgrConfigSection:
    git: GitSection = GitSection()
