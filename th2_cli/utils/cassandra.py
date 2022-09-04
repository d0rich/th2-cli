from cassandra.cluster import Cluster
from typing import List
from simple_term_menu import TerminalMenu
from th2_cli.utils import print_error, read_value
from cassandra.auth import PlainTextAuthProvider


def get_datacenters(host: str) -> List[str]:
    host = read_value('Enter host for connecting to Cassandra', 'Cassandra host', host)
    auth = PlainTextAuthProvider(
        username=read_value('Enter cassandra admin username', 'username', 'cassandra'),
        password=read_value('Enter cassandra admin password', 'password', 'cassandra')
    )
    cluster = Cluster([host], auth_provider=auth)
    try:
        session = cluster.connect('system')
    except:
        print_error('Cassandra cluster is unavailable')
        raise
    datacenters = list(map(lambda row: row.data_center, session.execute('select data_center from local;')))
    return datacenters


def choose_datacenter(host: str) -> str:
    datacenters = get_datacenters(host)
    terminal_menu = TerminalMenu(datacenters, title='Choose Cassandra datacenter:')
    node_index = terminal_menu.show()
    chosen_dc = datacenters[node_index]
    return chosen_dc
