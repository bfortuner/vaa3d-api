import os
from subprocess import call

from bigneuron_app.clients.constants import *
from bigneuron_app.clients import s3

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
	output_filename = input_filename + '.swc'
	input_file_path = os.path.abspath(input_filename)
	output_file_path = os.path.abspath(output_filename)
	return Vaa3dJob(input_filename, output_filename, input_file_path, output_file_path, 
		job_item.job.plugin, job_item.job.method, job_item.job.channel)

def run_job(job):
	print "Tracing neuron..."
	call([VAA3D_PATH, "-x", job.plugin, "-f", job.method,
		"-i", job.input_file_path, "-o", job.output_file_path])
	print "Trace complete!"

def cleanup(input_file_path, output_file_path):
	os.remove(input_file_path)
	os.remove(output_file_path)
	filelist = [ f for f in os.listdir(".") if f.endswith(".swc") ]
	for f in filelist:
		os.remove(os.path.abspath(f))

def test_job():
	job = Vaa3dJob(VAA3D_TEST_INPUT_FILE_1, VAA3D_TEST_OUTPUT_FILE_1,
		VAA3D_TEST_INPUT_FILE_1, VAA3D_TEST_OUTPUT_FILE_1)
	s3.download_file(job.input_filename, job.input_file_path, S3_INPUT_BUCKET)
	run_job(job)
	s3.upload_file(job.output_filename, job.output_file_path, S3_OUTPUT_BUCKET)
	cleanup(job.input_file_path, job.output_file_path)