import os, sys
import gzip
import zipfile
import subprocess
import shutil
import mimetypes

GZIP_FILE_EXT = '.gz'
ZIP_FILE_EXT = '.zip'

def call_process(command_str):
    p = subprocess.Popen(command_str, stdout=subprocess.PIPE, shell=True)
    output = p.communicate()[0]
    return output

def is_zipped_file(input_file_path):
	return zipfile.is_zipfile(input_file_path)

def zip_file(input_file_path, output_file_path):
	print "zip file: %s" % input_file_path
	zipped_file_path = output_file_path + ZIP_FILE_EXT
	zout = zipfile.ZipFile(zipped_file_path, "w")
	zout.write(input_file_path)
	zout.close()
	return zipped_file_path

def unzip_file(input_file_path, output_file_path):
	print "unzip file: %s" % input_file_path
	zin = zipfile.ZipFile(input_file_path, 'w')
	zin.write(output_file_path)
	zin.close()
	return output_file_path

def is_gzipped_file(input_file_path):
	filetype = mimetypes.guess_type(input_file_path)
	return filetype[1] == 'gzip'

def gzip_file(input_file_path, output_file_path):
	print "gzip file: %s" % input_file_path 
	gzipped_output_file_path = output_file_path + GZIP_FILE_EXT
	f_in = open(input_file_path, 'rb')
	f_out = gzip.open(gzipped_output_file_path, 'wb')
	f_out.writelines(f_in)
	f_out.close()
	f_in.close()
	return gzipped_output_file_path

def gunzip_file(input_file_path, output_file_path):
	print "gunzip file: %s" % input_file_path
	with gzip.open(input_file_path, 'rb') as f_in:
		f_in_content = f_in.read()
	f_out = open(output_file_path, 'w')
	f_out.write(f_in_content)
	f_out.close()
	return output_file_path

def compress_dir(dir_name, dir_path):
    call_process("tar -cvf %s %s" % (dir_name, dir_path))
    gzip_file(dir_name)
    os.remove(dir_name)
    return dir_name + GZIP_FILE_EXT

def cleanup(filepaths_list):
	print filepaths_list
	for filepath in filepaths_list:
		try:
			os.remove(filepath)
		except:
			print "File not found"


### Unit Tests ###

TEST_FILE_NAME = 'myfile.txt'
CURRENT_DIR = os.getcwd()
INPUT_FILE_PATH = os.path.join(CURRENT_DIR, TEST_FILE_NAME)
OUTPUT_FILE_PATH = os.path.join(CURRENT_DIR, TEST_FILE_NAME)

def create_test_file():
	test_file = open(INPUT_FILE_PATH, 'w')
	test_file.write("hello this is a file")
	test_file.close()

def print_file_contents(file_path):
	print "printing file contents"
	test_file = open(file_path, 'r+')
	print test_file.read()
	test_file.close()

def test_gzip_gunzip():
	create_test_file()
	gzip_file_path = gzip_file(INPUT_FILE_PATH, OUTPUT_FILE_PATH)
	assert is_gzipped_file(gzip_file_path) == True
	gunzip_file_path = gunzip_file(gzip_file_path, INPUT_FILE_PATH)
	print_file_contents(gunzip_file_path)
	cleanup([gzip_file_path, gunzip_file_path, INPUT_FILE_PATH])

def test_zip_unzip():
	create_test_file()
	zip_file_path = zip_file(INPUT_FILE_PATH, OUTPUT_FILE_PATH)
	assert is_zipped_file(zip_file_path) == True
	unzip_file_path = unzip_file(zip_file_path, OUTPUT_FILE_PATH)
	print_file_contents(unzip_file_path)
	cleanup([zip_file_path, unzip_file_path, INPUT_FILE_PATH])

def test_is_gzipped():
	create_test_file()
	gzip_file_path = gzip_file(INPUT_FILE_PATH, OUTPUT_FILE_PATH)
	assert is_gzipped_file(gzip_file_path) == True
	cleanup([gzip_file_path, INPUT_FILE_PATH])

def test_all():
	test_gzip_gunzip()
	test_zip_unzip()
	test_is_gzipped()
