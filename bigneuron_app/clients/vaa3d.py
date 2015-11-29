import os
from subprocess import call

from bigneuron_app.clients.constants import *
from bigneuron_app.clients import s3
from bigneuron_app.jobs.constants import OUTPUT_FILE_SUFFIXES, PLUGINS

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
	print "Tracing neuron..."
	input_file_path = os.path.abspath(job['input_filename'])
	output_file_path = os.path.abspath(job['output_filename'])
	cmd = " ".join([VAA3D_PATH, "-x", job['plugin'], "-f", job['method'], 
		"-i", input_file_path, "-p", str(job['channel'])])
	print "COMMAND: " + cmd
	call([VAA3D_PATH, "-x", job['plugin'], "-f", job['method'], "-i", 
		input_file_path, "-p", str(job['channel']), "-o", output_file_path])
	print "Trace complete!"

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
		os.remove(os.path.abspath(f))



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
	run_job(job.as_dict())
	s3.upload_file(job.output_filename, job.output_file_path, S3_OUTPUT_BUCKET)
	os.remove(job.output_file_path)