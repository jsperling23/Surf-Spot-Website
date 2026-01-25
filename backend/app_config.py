from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    secret_key: str
