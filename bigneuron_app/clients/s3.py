from boto import connect_s3
from boto.s3.connection import S3Connection
from boto.s3.key import Key


def get_connection():
	"""
	For EC2 hosts this is managed by roles
	IAM users must add the correct AWS tokens to their .bash_profile
	"""
	return connect_s3()

def get_bucket(connection, bucket_name):
	return connection.get_bucket(bucket_name, validate=False)

def download_file(filename, file_path, bucket):
	print "Downloading file..."
	k = Key(get_bucket(get_connection(), bucket))
	k.key = filename
	k.get_contents_to_filename(file_path)
	print "Downloading complete!"

def upload_file(filename, file_path, bucket):
	print "Uploading file..."
	k = Key(get_bucket(get_connection(), bucket))
	k.key = filename
	k.set_contents_from_filename(file_path)
	print "Upload complete!"

def get_all_files(bucket_name):
	bucket = get_bucket(get_connection(), bucket_name)
	files = bucket.list()
	filenames = []
	for f in files:
		filenames.append(f.name)
	return filenames