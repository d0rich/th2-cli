from dataclasses import dataclass


@dataclass
class CassandraConfigSection:
    host: str = '127.0.0.1'
    datacenter: str = 'datacenter1'