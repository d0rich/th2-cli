from dataclasses import dataclass


@dataclass
class GitSection:
    repository: str = ''
    http_auth_username: str = ''
    http_auth_password: str = ''
