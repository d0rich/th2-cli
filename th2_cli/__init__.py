__version__ = '1.5.0'

import fire
from th2_cli.cli import Th2Cli


def cli():
    fire.Fire(Th2Cli())
