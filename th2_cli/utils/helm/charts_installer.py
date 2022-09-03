from avionix import ChartDependency, ChartBuilder, ChartInfo
from typing import List


class ChartsInstaller:

    def __init__(self, namespace: str, th2_version: str):
        self.namespace = namespace
        self.th2_version = th2_version
        self.chart_info = ChartInfo(
            api_version='v2',
            name=f'th2--{namespace}',
            version=th2_version
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
        chart_builder = ChartBuilder(self.chart_info, [])
        chart_builder.install_chart({
            'namespace': self.namespace,
            "dependency-update": None
        })

