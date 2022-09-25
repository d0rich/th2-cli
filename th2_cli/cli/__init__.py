from th2_cli.install_versions import install_versions
from simple_term_menu import TerminalMenu


class Th2Cli:
    def install(self):
        all_versions = list(install_versions)
        version_index = TerminalMenu(all_versions, title='Choose th2 version to install').show()
        install_versions.get(all_versions[version_index])()

