from th2_cli.cli.install import install
from th2_cli.cli.delete import delete
from th2_cli.cli.status import status
from th2_cli.cli.version import get_th2cli_info
from th2_cli.cli.mgr import InfraMgr

import signal


def handler(signum, frame):
    print("Ctrl-C was pressed. Exiting ")
    exit(1)


class Th2Cli:

    mgr = InfraMgr()

    def version(self):
        get_th2cli_info()

    def install(self):
        signal.signal(signal.SIGINT, handler)
        install()

    def delete(self):
        signal.signal(signal.SIGINT, handler)
        delete()

    def status(self):
        status()
