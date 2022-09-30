from avionix import ChartDependency, ChartBuilder, ChartInfo
from th2_cli.utils import print_error
import tempfile
import shutil
from th2_cli import __version__


class ChartsInstaller:

    def __init__(self, namespace: str):
        self.namespace = namespace
        self.chart_info = ChartInfo(
            api_version='v2',
            name=f'th2--{namespace}',
            version=__version__
        )

    def add_helm_release(self, repo_name: str, chart_name: str, repo_url: str, version: str, values: dict = {}):
        self.chart_info.dependencies.append(ChartDependency(
            name=chart_name,
            version=version,
            repository=repo_url,
            local_repo_name=repo_name,
            values=values,
            is_local=False
        ))

    def install_charts(self):
        try:
            chart_builder = ChartBuilder(self.chart_info, [],
                                         keep_chart=False,
                                         output_directory=tempfile.gettempdir())
            shutil.rmtree(chart_builder.chart_folder_path, True)
            chart_builder.install_chart({
                'namespace': self.namespace,
                "dependency-update": None
            })
        except:
            print_error(f'Error occurred during deploy of "{self.namespace}" infrastructure')
