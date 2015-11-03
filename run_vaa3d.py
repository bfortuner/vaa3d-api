import os
from flask import Flask
from boto.s3.connection import S3Connection
from boto.s3.key import Key

TEST_BUCKET_NAME = 'vaa3d-test-data'
TEST_INPUT_FILENAME="tt2.v3draw"
TEST_OUTPUT_FILENAME="tt2.v3draw_x156_y372_z78_app2.swc"

MIME_TYPE="application/octet-stream"
VAA3D_PATH="/Applications/Vaa3d_V3.055_MacOSX10.9_64bit/Vaa3d.app/Contents/MacOS/vaa3d_script"
VAA3D_PLUGIN="libvn2_debug"
FUNC_NAME="app2"

app = Flask(__name__)
app.config.from_object('config.ProdConfig')

# Connect to bucket
conn = S3Connection(app.config['AWS_ACCESS_KEY'], app.config['AWS_SECRET_KEY'])
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
    print("Tracing neuron...");

    #call([VAA3D_PATH, "-x", VAA3D_PLUGIN, "-f", FUNC_NAME, "-i", input_filename, "-o", output_filename])
    print("Trace complete!")

def create_test_file():
    test = open(TEST_OUTPUT_FILENAME,'w')
    test.write("empty file")
    test.close()

def cleanup():
	os.remove(TEST_INPUT_FILENAME)
	os.remove(TEST_OUTPUT_FILENAME)

if __name__ == '__main__':
	create_test_file()
	download_file(TEST_INPUT_FILENAME)
	run_vaa3d_job(TEST_INPUT_FILENAME, TEST_OUTPUT_FILENAME)
	upload_file(TEST_OUTPUT_FILENAME)
	cleanup()