from th2_cli.cli.install import install

import signal


def handler(signum, frame):
    print("Ctrl-C was pressed. Exiting ")
    exit(1)


class Th2Cli:
    def install(self):
        signal.signal(signal.SIGINT, handler)
        install()
