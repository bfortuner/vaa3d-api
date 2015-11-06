import os
from subprocess import call

from application.clients.constants import *
from application.clients import s3

class Vaa3dJob():
	def __init__(self, options_dict=None):
		self.program = VAA3D_PATH
		self.plugin = options_dict['plugin']
		self.func = options_dict['func']
		self.input_filename = options_dict['input_filename']
		self.output_filename = options_dict['output_filename']
		self.input_file_path = options_dict['input_file_path']
		self.output_file_path = options_dict['output_file_path']

def run_job(job):
	print "Tracing neuron..."
	call([job.program, "-x", job.plugin, "-f", job.func, 
		"-i", job.input_file_path, "-o", job.output_file_path])
	print "Trace complete!"

def cleanup(input_file_path, output_file_path):
	os.remove(input_file_path)
	os.remove(output_file_path)
	filelist = [ f for f in os.listdir(".") if f.endswith(".swc") ]
	for f in filelist:
		os.remove(os.path.abspath(f))

def test_job():
	job = Vaa3dJob(VAA3D_TEST_JOB)
	s3.download_file(job.input_filename, job.input_file_path, S3_INPUT_BUCKET)
	run_job(job)
	s3.upload_file(job.output_filename, job.output_file_path, S3_OUTPUT_BUCKET)
	cleanup(job.input_file_path, job.output_file_path)