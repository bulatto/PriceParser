import importlib
import os


np = importlib.import_module(os.environ.get('DJANGO_SETTINGS_MODULE'))
