import os
import shutil
import pytest
from bigneuron_app.clients.vaa3d import *
from bigneuron_app.jobs.constants import *

@pytest.mark.skipif(True, reason="Too slow")
def test_all_plugins():
	#skip = ['MST_tracing','fastmarching_spanningtree','LCM_boost','Advantra','nctuTW','NeuroStalker','smartTrace','tips_GD']
	skip = ['nctuTW']
	START = 0
	STOP = 30
	filename = VAA3D_TEST_INPUT_FILE_5
	prepare_test_files_local([filename])
	i = START
	while i < STOP and i < len(JOB_TYPE_PLUGINS['Neuron Tracing']):
		plugin = JOB_TYPE_PLUGINS['Neuron Tracing'][i]
		if plugin not in skip:
			print "PLUGIN: " + plugin + ", FILENAME: " + filename 
			input_file_path = os.path.abspath(filename)
			print input_file_path
			run_plugin_local(plugin, PLUGINS[plugin], 
			filename, input_file_path)	
		i+=1
	cleanup_all([input_file_path])

#@pytest.mark.skipif(True, reason="Too slow")
def test_single_plugin():
	filenames = [VAA3D_TEST_INPUT_FILE_5, VAA3D_TEST_INPUT_FILE_1]
	prepare_test_files_local(filenames)
	plugin_name = 'MOST_tracing' #'MST_tracing'
	for f in filenames:
		input_file_path = os.path.abspath(f)
		run_plugin_local(plugin_name, PLUGINS[plugin_name], 
			f, input_file_path)
		cleanup_all([input_file_path])

#@pytest.mark.xfail(raises=Exception)
@pytest.mark.skipif(True, reason="Too slow")
def test_job_run_failures():
	filenames = [VAA3D_TEST_INPUT_FILE_4] #corrupt.tif
	prepare_test_files_local(filenames)
	plugin_name = 'MOST_tracing' #'MST_tracing'
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
	output_file_path, plugin_name, plugin['method']['default'], 
	plugin['settings']['params']['channel']['default'])
	run_job(job.as_dict())
	assert os.path.isfile(job.output_file_path)
	os.remove(job.output_file_path)

def prepare_test_files_local(filenames):
	for f in filenames:
		src = os.path.abspath("testdata/" + f)
		dest = os.path.abspath(f)
		shutil.copyfile(src, dest)