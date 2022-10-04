from dataclasses import dataclass
from th2_cli.utils import is_ip


@dataclass
class KubernetesConfigSection:
    pvs_node: str = ''
    host: str = ''

    def hostname(self) -> str:
        if is_ip(self.host):
            return ''
        return self.host
