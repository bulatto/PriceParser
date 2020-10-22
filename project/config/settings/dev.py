from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS += [
    '127.0.0.1',
]

# if LOG_PATH and os.path.isdir(LOG_PATH):
#     # Журналирование SQL-запросов
#     LOGGING['formatters']['sql'] = {
#         '()': '.'.join((__name__, '_SQLFormatter')),
#         'format': '[%(asctime)s] (%(duration).3f)\n%(sql)s\n'
#     }
#     LOGGING['handlers']['sql'] = {
#         'level': 'DEBUG',
#         'class': 'logging.handlers.RotatingFileHandler',
#         'formatter': 'sql',
#         'filename': os.path.join(LOG_PATH, 'sql.log'),
#         'backupCount': 1,
#         'maxBytes': 10 * 1024 * 1024,  # 10 Mb
#     }
#     LOGGING['loggers']['django.db.backends']['handlers'] = ['sql']
#
#     MIDDLEWARE.insert(0, 'kinder.core.middleware.SqlLoggingMiddleware')
