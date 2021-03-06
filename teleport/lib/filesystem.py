import re
import os.path
import shutil
from datetime import date

from django.conf import settings

TEMP_FILE_STORE = settings.TEMP_FILE_STORE

def parent_path(path):
    return os.path.dirname(path)

def file_name(path):
    return os.path.basename(path)

def save_from_upload(path, file_obj):
    temp_path = os.path.join(TEMP_FILE_STORE, file_name(path))
    fp = open(temp_path, 'w')
    for chunk in file_obj.chunks():
        fp.write(chunk)
    fp.close()
    return temp_path

def get_mod_date(path):
    epoch_seconds = os.path.getmtime(path)
    return date.fromtimestamp(epoch_seconds)

def file_info(path):
    return {'name': file_name(path),
            'path': parent_path(path),
            'last_modified': get_mod_date(path),
            'size': os.path.getsize(path)}