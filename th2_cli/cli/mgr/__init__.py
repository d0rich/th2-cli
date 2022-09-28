from th2_cli.cli.mgr.logs import logs
from th2_cli.cli.mgr.status import status


class InfraMgr:
    def logs(self):
        logs()

    def status(self):
        status()
