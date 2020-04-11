from parsing.site_config.config_parser import (
    ConfigParseHelper, SiteConfigParser)
from .settings import SITE_CONFIG_PATH


site_config = SiteConfigParser()
site_config.read(SITE_CONFIG_PATH)
# Конфигурация всех сайтов
all_sites_config = site_config.parse_sites_config()
