import os

from config.settings.base import PROJECT_SETTINGS_DIR


# Расположение конфигураций сайтов
SITE_CONFIG_PATH = os.path.join(PROJECT_SETTINGS_DIR, 'site_config.txt')
if not os.path.exists(SITE_CONFIG_PATH):
    # Если файла нет, создаётся пустой файл
    open(SITE_CONFIG_PATH, 'w').close()
