import fire
from th2_cli.cli import Th2Cli


def cli():
    fire.Fire(Th2Cli())


if __name__ == '__main__':
    cli()
