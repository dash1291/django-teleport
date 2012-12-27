import os, os.path
import shutil

class StorageLocal():
    def __init__(self, storage_path):
        self.storage_path = storage_path

    def upload_file(self, local_path, remote_path):
        APP_STORAGE_PATH = self.storage_path
        dest = os.path.join(APP_STORAGE_PATH, 'files', remote_path)
        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))
        shutil.move(local_path, dest)
     
    def create_archive(self, path):
        APP_STORAGE_PATH = self.storage_path
        shutil.make_archive(os.path.join(APP_STORAGE_PATH, 'archives',
            os.path.basename(path)), 'zip',
            os.path.join(APP_STORAGE_PATH, 'files', path))
        return os.path.join('archives', os.path.basename(path) + '.zip')
