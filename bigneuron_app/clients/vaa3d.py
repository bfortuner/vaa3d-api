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

def build_vaa3d_job(job_item):
	input_filename = job_item.filename
	output_filename = input_filename + job_item.job.output_file_suffix
	input_file_path = os.path.abspath(input_filename)
	output_file_path = os.path.abspath(output_filename)
	return Vaa3dJob(input_filename, output_filename, input_file_path, output_file_path, 
		job_item.job.plugin, job_item.job.method, job_item.job.channel)

def run_job(job):
	print "Tracing neuron..."
	print job.plugin
	print job.method
	print job.input_file_path
	cmd = " ".join([VAA3D_PATH, "-x", job.plugin, "-f", job.method, "-i", job.input_file_path, "-p", str(job.channel)])
	print "COMMAND: " + cmd
	call([VAA3D_PATH, "-x", job.plugin, "-f", job.method, "-i", job.input_file_path, "-p", str(job.channel)])
	print "Trace complete!"

def cleanup(input_file_path, output_file_path):
	os.remove(input_file_path)
	os.remove(output_file_path)
	filelist = [ f for f in os.listdir(".") if f.endswith(".swc") ]
	for f in filelist:
		os.remove(os.path.abspath(f))

def cleanup_all(list_of_file_paths):
	filelist = [ f for f in os.listdir(".") if f.endswith(".swc") ]
	filelist.extend(list_of_file_paths)
	for f in filelist:
		os.remove(os.path.abspath(f))

def test_jobs():
	# Download S3 Test Data
	input_filename = VAA3D_TEST_INPUT_FILE_1
	input_file_path = os.path.abspath(input_filename)
	s3.download_file(input_filename, input_file_path, S3_INPUT_BUCKET)

	# Loop through plugins and run Vaa3D job
	#test_plugin(PLUGINS[1], input_filename, input_file_path)
	#for plugin in PLUGINS:
#		test_plugin(plugin, input_filename, input_file_path)

	cleanup_all([input_file_path])


def test_plugin(plugin, input_filename, input_file_path):
	output_filename = input_filename + OUTPUT_FILE_SUFFIXES[plugin['name']]
	output_file_path = os.path.abspath(output_filename)
	job = Vaa3dJob(input_filename, output_filename, input_file_path,
	output_file_path, plugin['name'], plugin['method']['default'], 1)
	run_job(job)
	s3.upload_file(job.output_filename, job.output_file_path, S3_OUTPUT_BUCKET)
	os.remove(job.output_file_path)