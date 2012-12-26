from django.conf import settings as settings
from teleport.lib.storage_adapters import storage_local

def get_adapter():
    teleport_settings = settings.TELEPORT
    storage_type = teleport_settings['storage_type']

    if storage_type == 'local':
        storage_path = teleport_settings['storage_path']
        return storage_local.StorageLocal(storage_path)