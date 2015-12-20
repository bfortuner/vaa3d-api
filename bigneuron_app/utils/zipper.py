import os, sys
import gzip
import zipfile
import subprocess
import shutil
import mimetypes
import ntpath

GZIP_FILE_EXT = '.gz'
ZIP_FILE_EXT = '.zip'

def is_compressed_filename(filename):
	file_parts = filename.split(".")
	return file_parts[-1] in ("zip","gz")

def call_process(command_str):
    p = subprocess.Popen(command_str, stdout=subprocess.PIPE, shell=True)
    output = p.communicate()[0]
    return output

def get_files_in_zip_dir(input_file_path):
	zipped_files = zipfile.ZipFile(input_file_path, 'r')
	return zipped_files

def is_zip_file(input_file_path):
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
	for filepath in filepaths_list:
		try:
			os.remove(filepath)
		except:
			print "File not found"


def expand_zip_archive(zip_archive, output_dir):
	if not os.path.exists(output_dir):   #we could use this replicate the zip dir structure 
		os.makedirs(output_dir)
	for member in zip_archive.namelist():
		filename = ntpath.basename(member)
		# skip directories
		if not filename:
			continue
		# skip hidden files
		if filename.startswith('.'):
			continue
		ouput_file_path = os.path.join(output_dir, filename)
		extract_file_from_archive(zip_archive, member, ouput_file_path)

def extract_file_from_archive(zip_archive, filename, output_file_path):
	source = zip_archive.open(filename)
	target = file(output_file_path, 'w+')
	with source, target:
		shutil.copyfileobj(source, target)
	target.close()

