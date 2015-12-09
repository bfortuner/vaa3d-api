import os
import shutil
import time
import subprocess32 as subprocess
import traceback
from bigneuron_app import items_log
from bigneuron_app.clients.constants import *
from bigneuron_app.utils.constants import USER_JOB_LOG_EXT
from bigneuron_app.clients import s3
from bigneuron_app.jobs.constants import OUTPUT_FILE_SUFFIXES, PLUGINS
from bigneuron_app.utils.constants import JOB_ITEMS_LOG_FILE
from bigneuron_app.utils.command import Command

class Vaa3dJob():
	def __init__(self, input_filename, output_filename, input_file_path, 
		output_file_path, plugin=VAA3D_DEFAULT_PLUGIN, method=VAA3D_DEFAULT_FUNC, channel=1):
		self.plugin = plugin
		self.method = method
		self.channel = channel
		self.input_filename = input_filename
		self.output_filename = output_filename
		self.input_file_path = input_file_path
		self.output_file_path = output_file_path

	def as_dict(self):
		return self.__dict__

def build_vaa3d_job(job_item):
	input_filename = job_item.filename
	output_filename = input_filename + job_item.job.output_file_suffix
	input_file_path = os.path.abspath(input_filename)
	output_file_path = os.path.abspath(output_filename)
	return Vaa3dJob(input_filename, output_filename, input_file_path, output_file_path, 
		job_item.job.plugin, job_item.job.method, job_item.job.channel)

def run_job(job):
	items_log.info("Tracing neuron... ")
	input_file_path = os.path.abspath(job['input_filename'])
	output_file_path = os.path.abspath(job['output_filename'])
	log_file_path = output_file_path + USER_JOB_LOG_EXT
	logfile = open(log_file_path, "w")
	cmd_args = [VAA3D_PATH, "-x", job['plugin'], "-f", job['method'], 
		"-i", input_file_path, "-p", str(job['channel']), "-o", output_file_path]
	items_log.info("Running Command: " + " ".join(cmd_args))
	start_time = int(time.time())
	max_runtime_sec = get_timeout(input_file_path)
	cmd = Command(cmd_args, logfile)
	try:
		status = cmd.run(max_runtime_sec)
		items_log.info("Trace complete!")
		runtime = int(time.time()) - start_time
		if status == "OK":
			logfile.write("\nActual Runtime = " + str(runtime) + " seconds")
			items_log.info("\nActual Runtime = " + str(runtime) + " seconds")
		elif status == "TIMEOUT":
			logfile.write("\nJOB RAN TOO LONG. KILLING. Max Runtime is " + str(max_runtime_sec) + " seconds")
			items_log.info("\nJOB RAN TOO LONG. KILLING. Max Runtime is " + str(max_runtime_sec) + " seconds")
	except Exception, e:
		raise Exception(traceback.format_exc())
	finally:
		logfile.close()

def get_timeout(file_path):
	"""
	Returns filesize in bytes
	1000 bytes = 1 KB
	1000000 bytes = 1 MB
	APP1 = 3.5 secs / MB
	APP1 = .0000033457 secs / byte
	"""
	MIN_RUNTIME = 10 #sec
	BYTES_PER_MEGABYTE = 1000000
	SECONDS_PER_BYTE = .0000033457
	BUFFER_MULTIPLIER = 5
	file_size_bytes = os.stat(file_path).st_size
	items_log.info("Filesize in MB " + str(file_size_bytes/BYTES_PER_MEGABYTE))
	estimated_runtime = SECONDS_PER_BYTE * file_size_bytes
	items_log.info("Estimated Runtime " + str(int(estimated_runtime)) + " seconds")
	timeout = max(MIN_RUNTIME, int(estimated_runtime * BUFFER_MULTIPLIER))
	items_log.info("Runtime w Buffer " + str(timeout) + " seconds")
	return timeout

def cleanup(input_file_path, output_file_path):
	os.remove(input_file_path)
	os.remove(output_file_path)
	filelist = [ f for f in os.listdir(".") if f.endswith(".swc") ]
	for f in filelist:
		os.remove(os.path.abspath(f))

def cleanup_all(list_of_filenames):
	filelist = [ f for f in os.listdir(".") if f.endswith(".swc") ]
	filelist.extend(list_of_filenames)
	for f in filelist:
		try:
			os.remove(os.path.abspath(f))
		except Exception, e:
			items_log.info("File to remove not found " + str(e))


## Unit Tests ##

def test_plugins():
	# Download S3 Test Data
	filenames = [VAA3D_TEST_INPUT_FILE_1]
	for f in filenames:
		input_filename = f
		input_file_path = os.path.abspath(f)
		s3.download_file(f, os.path.abspath(f), S3_INPUT_BUCKET)

	# Test all plugins
	for name in PLUGINS.keys():
		print "Running plugin : " + name
		test_plugin(name, PLUGINS[name], input_filename, input_file_path)

	cleanup_all(filenames)

def prepare_test_files_local(filenames):
	for f in filenames:
		src = os.path.abspath("testdata/" + f)
		dest = os.path.abspath(f)
		shutil.copyfile(src, dest)

def test_single_plugin_local():
	filenames =  ["corruptfile.tif", VAA3D_TEST_INPUT_FILE_1]
	prepare_test_files_local(filenames)
	plugin_name = 'Vaa3D_Neuron2' #'MST_tracing'
	for f in filenames:
		input_file_path = os.path.abspath(f)
		test_plugin_local(plugin_name, PLUGINS[plugin_name], 
			f, input_file_path)

def test_plugin_local(plugin_name, plugin, input_filename, input_file_path):
	output_filename = input_filename + OUTPUT_FILE_SUFFIXES[plugin_name]
	output_file_path = os.path.abspath(output_filename)
	job = Vaa3dJob(input_filename, output_filename, input_file_path,
	output_file_path, plugin_name, plugin['method']['default'], 1)
	print "running job"
	try:
		run_job(job.as_dict())
		os.remove(job.output_file_path)
	except Exception, e:
		print traceback.format_exc()
	finally:
		print "ran job"

def prepare_test_files(filenames):
	for f in filenames:
		s3.download_file(f, os.path.abspath(f), S3_INPUT_BUCKET)

def test_single_plugin():
	input_filename =  VAA3D_TEST_INPUT_FILE_1
	input_file_path = os.path.abspath(input_filename)
	prepare_test_files([input_filename])
	plugin_name = 'Vaa3D_Neuron2' #'MST_tracing'
	test_plugin(plugin_name, PLUGINS[plugin_name], 
		input_filename, input_file_path)

def test_plugin(plugin_name, plugin, input_filename, input_file_path):
	output_filename = input_filename + OUTPUT_FILE_SUFFIXES[plugin_name]
	output_file_path = os.path.abspath(output_filename)
	job = Vaa3dJob(input_filename, output_filename, input_file_path,
	output_file_path, plugin_name, plugin['method']['default'], 1)
	print "running job"
	run_job(job.as_dict())
	print "running job"
	s3.upload_file(job.output_filename, job.output_file_path, S3_OUTPUT_BUCKET)
	os.remove(job.output_file_path)

def cleanup_all_filename_not_found():
	filenames = ["fakefile.txt"]
	cleanup_all(filenames)
