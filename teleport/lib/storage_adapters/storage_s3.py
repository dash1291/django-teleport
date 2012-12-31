from boto.s3.bucket import Bucket
from boto.s3.connection import S3Connection
from boto.s3.key import Key

class StorageS3():
    def __init__(self, *args, **kwargs):
        self.s3_key = kwargs['key']
        self.s3_secret = kwargs['secret']
        self.s3_bucket_name = kwargs['bucket']

        self.make_connection()

    def make_connection(self):
        conn = S3Connection(self.s3_key, self.s3_secret)
        self.bucket = Bucket(conn, self.s3_bucket_name)

    def upload_file(self, local_path, remote_path):
        key = Key(self.bucket, remote_path)
        key.set_contents_from_file(file(str(local_path)))
        key.set_acl('public-read')

    def delete_file(self, remote_path):
        self.bucket.delete_key(remote_path)