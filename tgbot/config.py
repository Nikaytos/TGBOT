from dataclasses import dataclass

from environs import Env
from configparser import ConfigParser


@dataclass
class Dictionary:
    emails: dict[str, str]
    lectures: dict[str, str]
    practicums: dict[str, str]
    labs: dict[str, str]
    url: dict[str, str]


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    dict: Dictionary
    misc: Miscellaneous


def load_config(path: str = None, path2: str = None):
    env = Env()
    env.read_env(path)
    config_info = ConfigParser()
    config_info.optionxform = lambda option: option
    config_info.read(path2, encoding='utf-8')

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        dict=Dictionary(
            emails=dict(config_info.items('emails')),
            lectures=dict(config_info.items('lec')),
            practicums=dict(config_info.items('prac')),
            labs=dict(config_info.items('lab')),
            url=dict(config_info.items('url'))
        ),
        misc=Miscellaneous()
    )
