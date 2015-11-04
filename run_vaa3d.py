import os
from subprocess import call
from boto.s3.connection import S3Connection
from boto.s3.key import Key

AWS_ACCESS_KEY = os.getenv('VAA3D_AWS_ACCESS_KEY', 'password')
AWS_SECRET_KEY = os.getenv('VAA3D_AWS_SECRET_KEY', 'password')

TEST_BUCKET_NAME = 'vaa3d-test-data'
TEST_INPUT_FILENAME='tt2.v3draw'
TEST_OUTPUT_FILENAME='output.swc'

VAA3D_PATH='/Applications/vaa3d/vaa3d64.app/Contents/MacOS/vaa3d64'
VAA3D_PLUGIN='libvn2_debug'
FUNC_NAME='app2'
#/Applications/vaa3d/vaa3d64.app/Contents/MacOS/vaa3d64 -x libvn2_debug -f app2 -i tt2.v3draw -o output.swc

# Connect to bucket
conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
bucket = conn.get_bucket('vaa3d-test-data', validate=False)

def download_file(filename):
	print "Downloading file..."
	k = Key(bucket)
	k.key = filename
	k.get_contents_to_filename(filename)
	print "Downloading complete!"

def upload_file(filename):
	print "Uploading file..."
	k = Key(bucket)
	k.key = filename
	k.set_contents_from_filename(filename)
	print "Upload complete!"

def run_vaa3d_job(input_filename, output_filename):
    print "Tracing neuron..."
    call([VAA3D_PATH, "-x", VAA3D_PLUGIN, "-f", FUNC_NAME, "-i", input_filename, "-o", output_filename])
    print "Trace complete!"

def cleanup():
	os.remove(TEST_INPUT_FILENAME)
	os.remove(TEST_OUTPUT_FILENAME)

if __name__ == '__main__':
	download_file(TEST_INPUT_FILENAME)
	run_vaa3d_job(TEST_INPUT_FILENAME, TEST_OUTPUT_FILENAME)
	upload_file(TEST_OUTPUT_FILENAME)
	cleanup()