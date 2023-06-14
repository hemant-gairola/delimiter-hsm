import configparser
from functools import lru_cache
from src.utils.constants import CONFIG_FILE_PATH


@lru_cache
def get_config() -> configparser.ConfigParser:
    """
    Responsible for reading the default config file

    Returns:
        ConfigParser object which can be called as a dictionary
    """
    parser = configparser.ConfigParser()
    parser.read(CONFIG_FILE_PATH)
    return parser
