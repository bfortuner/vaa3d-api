import os
import shutil
import pytest
from bigneuron_app.utils.zipper import *

TEST_FILE_NAME = 'myfile.txt'
CURRENT_DIR = os.getcwd()
INPUT_FILE_PATH = os.path.join(CURRENT_DIR, TEST_FILE_NAME)
OUTPUT_FILE_PATH = os.path.join(CURRENT_DIR, TEST_FILE_NAME)

@pytest.fixture
def setup(request):
    print('setting up tests')
    create_test_file()
    def teardown():
        print('teardown tests')
        cleanup_test_files()
    request.addfinalizer(teardown)

def create_test_file():
	test_file = open(INPUT_FILE_PATH, 'w')
	test_file.write("hello this is a file")
	test_file.close()

def cleanup_test_files(filenames=[]):
	zipfiles = [ f for f in os.listdir(".") if f.endswith(".zip") ]
	gzipfiles = [ f for f in os.listdir(".") if f.endswith(".gz") ]
	filenames.extend(zipfiles)
	filenames.extend(gzipfiles)
	filenames.append(INPUT_FILE_PATH)
	print "Files " + str(filenames)
	for f in filenames:
		try:
			os.remove(os.path.abspath(f))
		except Exception, e:
			print "File to remove not found " + str(e)

def test_is_compressed_filename(setup):
	files = [['mytest.zip',True],
			['mytest.mytest.zip',True],
			['mytest.mytest',False],
			['mytest.gz',True]]
	for f in files:
		is_compressed = is_compressed_filename(f[0])
		assert(is_compressed == f[1]) 

def test_gzip_gunzip(setup):
	gzip_file_path = gzip_file(INPUT_FILE_PATH, OUTPUT_FILE_PATH)
	assert is_gzipped_file(gzip_file_path) == True
	gunzip_file_path = gunzip_file(gzip_file_path, INPUT_FILE_PATH)

def test_zip_unzip(setup):
	zip_file_path = zip_file(INPUT_FILE_PATH, OUTPUT_FILE_PATH)
	assert is_zip_file(zip_file_path) == True
	unzip_file_path = unzip_file(zip_file_path, OUTPUT_FILE_PATH)

def test_is_gzipped(setup):
	gzip_file_path = gzip_file(INPUT_FILE_PATH, OUTPUT_FILE_PATH)
	assert is_gzipped_file(gzip_file_path) == True
