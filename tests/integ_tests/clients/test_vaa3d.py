import os
import shutil
import pytest
from bigneuron_app.clients.vaa3d import *


#@pytest.mark.skipif(True, reason="Too slow")
def test_single_plugin_local():
	filenames =  ["corruptfile.tif", VAA3D_TEST_INPUT_FILE_1]
	prepare_test_files_local(filenames)
	plugin_name = 'Vaa3D_Neuron2' #'MST_tracing'
	for f in filenames:
		input_file_path = os.path.abspath(f)
		run_plugin_local(plugin_name, PLUGINS[plugin_name], 
			f, input_file_path)
		cleanup_all([input_file_path])

@pytest.mark.xfail(raises=Exception)
def test_try_finally():
	try:
		raise Exception("hey there mister")
	finally:
		print "DO this regardless of exception"

def test_try_finally_exception():
	with pytest.raises(Exception):
		try:
			raise Exception("hey there mister")
		finally:
			print "DO this regardless of exception"

# Helpers

def run_plugin_local(plugin_name, plugin, input_filename, input_file_path):
	output_filename = input_filename + OUTPUT_FILE_SUFFIXES[plugin_name]
	output_file_path = os.path.abspath(output_filename)
	job = Vaa3dJob(input_filename, output_filename, input_file_path,
	output_file_path, plugin_name, plugin['method']['default'], 1)
	try:
		run_job(job.as_dict())
		os.remove(job.output_file_path)
	except Exception, e:
		print traceback.format_exc()
	finally:
		print "ran job"

def prepare_test_files_local(filenames):
	for f in filenames:
		src = os.path.abspath("testdata/" + f)
		dest = os.path.abspath(f)
		shutil.copyfile(src, dest)