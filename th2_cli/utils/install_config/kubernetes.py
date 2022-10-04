from dataclasses import dataclass
from th2_cli.utils import is_ip

NODE_DEFAULT_VALUE = HOST_DEFAULT_VALUE = ''


@dataclass
class KubernetesConfigSection:
    pvs_node: str = NODE_DEFAULT_VALUE
    host: str = HOST_DEFAULT_VALUE

    def hostname(self) -> str:
        if is_ip(self.host):
            return ''
        return self.host

    def pvs_node_is_default(self) -> bool:
        return self.pvs_node == NODE_DEFAULT_VALUE

    def host_is_default(self) -> bool:
        return self.host == HOST_DEFAULT_VALUE
