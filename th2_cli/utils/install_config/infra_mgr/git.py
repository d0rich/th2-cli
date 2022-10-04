from dataclasses import dataclass


REPO_DEFAULT_VALUE = \
    USERNAME_DEFAULT_VALUE = \
    PASSWORD_DEFAULT_VALUE = ''


@dataclass
class GitSection:
    repository: str = REPO_DEFAULT_VALUE
    http_auth_username: str = USERNAME_DEFAULT_VALUE
    http_auth_password: str = PASSWORD_DEFAULT_VALUE

    def repository_is_default(self) -> bool:
        return self.repository == REPO_DEFAULT_VALUE

    def http_auth_username_is_default(self) -> bool:
        return self.http_auth_username == USERNAME_DEFAULT_VALUE

    def http_auth_password_is_default(self) -> bool:
        return self.http_auth_password == PASSWORD_DEFAULT_VALUE
