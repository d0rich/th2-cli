from dataclasses import dataclass

HOST_DEFAULT_VALUE = '127.0.0.1'
DC_DEFAULT_VALUE = 'datacenter1'


@dataclass
class CassandraConfigSection:
    host: str = HOST_DEFAULT_VALUE
    datacenter: str = DC_DEFAULT_VALUE

    def host_is_default(self) -> bool:
        return self.host == HOST_DEFAULT_VALUE

    def datacenter_is_default(self) -> bool:
        return self.datacenter == DC_DEFAULT_VALUE
