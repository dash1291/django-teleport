from settings import teleport
from teleport.lib.storage_adapters import *

def get_adapter():
	storage_type = teleport['storage_type']

	if storage_type == 'local':
		storage_path = teleport['storage_path']
		return storage_local