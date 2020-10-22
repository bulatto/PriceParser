# Standard Library
import logging.handlers
import os
import sys
import traceback

# Vendor Library
from django.http import HttpRequest
from django.http import HttpResponseServerError
from django.template.loader import get_template
from django.utils.encoding import force_str
from django.views.decorators.csrf import requires_csrf_token


# __all__ = ['init_logging', 'catch_error_500', 'info', 'error', 'debug', 'warning']


def init_logging(logs_path, debug_mode=True):
    """
    Инициализация логирования. Срабатывает только один раз.
    Каждый error level записывается в свой лог.
    Нужно добавлять в settings.py или manage.py
    """
    if hasattr(logging, "set_up_done"):
        return

    if not os.path.exists(logs_path):
        os.mkdir(logs_path)

    loggers = [('root',         logging.NOTSET, 'root.log'),
               ('error_logger', logging.ERROR,  'error.log'),
               ('info_logger',  logging.INFO,   'info.log')]

    if debug_mode:
        loggers.extend([('debug_logger',  logging.DEBUG,   'debug.log'),
                        ('warning_logger',  logging.DEBUG,   'warning.log')])

    formatter = logging.Formatter("[%(asctime)s] %(message)s")
    formatter.datefmt = '%Y-%m-%d %H:%M:%S'
    for lname, level, fname in loggers:
        t = logging.getLogger(lname)
        t.setLevel(level)
        handler = logging.handlers.TimedRotatingFileHandler(
            os.path.join(logs_path, fname), when='D', encoding='utf-8')
        handler.setFormatter(formatter)
        t.addHandler(handler)

    logging.set_up_done = True
#
#
# def get_session_info(request):
#     '''
#     Возвращает строку для лога с информацией о запросе
#     '''
#     if request is None or not isinstance(request, HttpRequest):
#         return ''
#     # Адрес запроса
#     result = 'URL: ' + request.get_full_path() + ' (' + request.method + ')'
#     # Юзер
#     if hasattr(request, 'user'):
#         user = request.user
#         if user and user.is_authenticated():
#             result += ' - ' + user.email + ', ' + user.get_full_name()
#     return result + '. '
#
# #====================== ФУНКЦИИ АНАЛОГИЧНЫЕ LOGGING =====================
# # Если передать именованный аргумент request = ... , то к сообщению будет
# # добавлена информация о запросе
# #========================================================================
#
#
# def info(msg, *args, **kwargs):
#     log = logging.getLogger('info_logger')
#     msg = get_session_info(kwargs.get('request', None)) + msg
#     log.info(msg)
#
#
# def error(msg, *args, **kwargs):
#     log = logging.getLogger('error_logger')
#     msg = get_session_info(kwargs.get('request', None)) + msg
#     log.error(msg)
#
#
# def debug(msg, *args, **kwargs):
#     '''
#     Выводит информацию в debug-log только в случае включенного режима отладки
#     '''
#     log = logging.getLogger('debug_logger')
#     msg = get_session_info(kwargs.get('request', None)) + msg
#     log.debug(msg)
#
#
# def exception(msg='', *args, **kwargs):
#     #Не желаемые ключи логирования
#     black_list = ['win',
#                   # Запрос браузера
#                   'request',
#                   # Запрос в БД (sql)
#                   'query']
#
#     log = logging.getLogger('error_logger')
#     msg = get_session_info(kwargs.get('request', None)) + 'Message: ' + msg + '\n'
#
#     # FIXME: Отрефаторить нахер!!
#     exception_info = sys.exc_info()
#     try:
#         e_type, e_value, e_traceback = exception_info
#         e_vars = e_traceback.tb_frame.f_locals
#         res = ['Variables:\n']
#
#         if e_traceback.tb_frame.f_code.co_name != '<module>':
#             for key, val in e_vars.items():
#                 if key in black_list:
#                     continue
#
#                 res.append('%s: %s\n'.rjust(6) % (key, force_str(val) if isinstance(val, str) else val))
#                 if hasattr(val, '__dict__'):
#                     for obj_key, obj_val in val.__dict__.items():
#                         if obj_key[0] != '_' and obj_key not in black_list:
#                             res.append('%s: %s\n'.rjust(12)
#                                        % (obj_key, force_str(obj_val) if isinstance(obj_val, str) else obj_val))
#         else:
#             res = []
#
#         e_vars_str = ''.join(res)
#         tb = traceback.format_exception(e_type, e_value, e_traceback)
#
#         err_message = '\n %s %s %s' % (force_str(msg), force_str(''.join(tb)), force_str(e_vars_str))
#         log.error(err_message)
#     except:
#         _old_good_exception(msg, exception_info, *args, **kwargs)
#
#
# def _old_good_exception(msg, exception_info, *args, **kwargs):
#     """
#     Старый добрый способ вывода ошибки, без переменных, зато надежный.
#       msg - гневное сообщение разработчикам
#       exception_info - информация о оригинальной ошибке
#     """
#     log = logging.getLogger('error_logger')
#     try:
#         tb = traceback.format_exception(*exception_info)
#         log.error(force_str(get_session_info(kwargs.get('request')) + msg) + '\n' + ''.join(tb))
#     except:
#         try:
#             log.error(force_str(msg) + '\n')
#         except:
#             log.error('Некорректная работа логгера')
#
#
# def warning(msg, *args, **kwargs):
#     log = logging.getLogger('warning_logger')
#     msg = get_session_info(kwargs.get('request', None)) + msg
#     log.warning(msg)