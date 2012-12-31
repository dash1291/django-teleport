from django.conf import settings as settings

from teleport.lib.storage_adapters import storage_local, storage_s3

def get_adapter():
    teleport_settings = settings.TELEPORT
    storage_type = teleport_settings['storage_type']

    if storage_type == 'local':
        storage_path = teleport_settings['storage_path']
        return storage_local.StorageLocal(storage_path)

    elif storage_type == 's3':
    	return storage_s3.StorageS3(key=teleport_settings['key'],
    								secret=teleport_settings['secret'],
    								bucket=teleport_settings['bucket'])