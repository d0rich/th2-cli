__version__ = '0.1.0'

import fire
from th2_cli.cli import Th2Cli


def cli():
    fire.Fire(Th2Cli())
