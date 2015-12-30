import os
import shutil
import pytest
from bigneuron_app.clients.vaa3d import *
from bigneuron_app.utils import timeout
from bigneuron_app.jobs.constants import *

@pytest.mark.skipif(True, reason="Too slow")
def test_all_plugins():
	#skip = ['MST_tracing','fastmarching_spanningtree','LCM_boost','Advantra','nctuTW','NeuroStalker','smartTrace','tips_GD']
	skip = [] #['nctuTW']
	START = 0
	STOP = 30
	filename = VAA3D_TEST_INPUT_FILE_5
	prepare_test_files_local([filename])
	i = START
	errored = []
	while i < STOP and i < len(JOB_TYPE_PLUGINS['Neuron Tracing']):
		plugin = JOB_TYPE_PLUGINS['Neuron Tracing'][i]
		if plugin not in skip:
			try:
				print "PLUGIN: " + plugin + ", FILENAME: " + filename 
				input_file_path = os.path.abspath(filename)
				max_runtime = timeout.get_timeout_from_file(input_file_path)
				print input_file_path
				run_plugin_local(plugin, PLUGINS[plugin], 
				filename, input_file_path, max_runtime)	
			except Exception, e:
				print "####### Plugin " + plugin + " failed ########\n" + str(e)
				errored.append([plugin,filename])
		i+=1
	cleanup_all([input_file_path])
	print "##### Plugins Errored ###### "
	for p in errored:
		print p

def test_single_plugin():
	filenames = [VAA3D_TEST_INPUT_FILE_5, VAA3D_TEST_INPUT_FILE_1]
	prepare_test_files_local(filenames)
	plugin_name = 'Advantra' #'MST_tracing'
	for f in filenames:
		input_file_path = os.path.abspath(f)
		max_runtime = timeout.get_timeout_from_file(input_file_path)
		run_plugin_local(plugin_name, PLUGINS[plugin_name], 
			f, input_file_path, max_runtime)
		cleanup_all([input_file_path])

@pytest.mark.xfail(raises=Exception)
def test_job_run_failures():
	filenames = [VAA3D_TEST_INPUT_FILE_4] #corrupt.tif
	prepare_test_files_local(filenames)
	plugin_name = 'Vaa3D_Neuron2' #'MST_tracing'
	for f in filenames:
		input_file_path = os.path.abspath(f)
		run_plugin_local(plugin_name, PLUGINS[plugin_name], 
			f, input_file_path, 10)
		cleanup_all([input_file_path])

def test_build_cmd_args():
	plugin_name = 'Vaa3D_Neuron2'
	job = Vaa3dJob("input_filename", "output_filename", "input_file_path",
		"output_file_path", plugin_name, "method", "channel").as_dict()
	args = build_cmd_args(job, job['input_file_path'], job['output_file_path'])
	assert "-p" in args
	assert "channel" in args

	plugin_name = 'nctuTW' #cannot include -p flag
	job = Vaa3dJob("input_filename", "output_filename", "input_file_path",
		"output_file_path", plugin_name, "method", "channel").as_dict()
	args = build_cmd_args(job, job['input_file_path'], job['output_file_path'])
	assert "-p" not in args
	assert "channel" not in args
	
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

def run_plugin_local(plugin_name, plugin, input_filename, input_file_path, max_runtime):
	output_filename = input_filename + OUTPUT_FILE_SUFFIXES[plugin_name]
	output_file_path = os.path.abspath(output_filename)
	if PLUGINS[plugin_name]['settings']:
		channel = plugin['settings']['params']['channel']['default']
	else:
		channel = 1
	job = Vaa3dJob(input_filename, output_filename, input_file_path,
	output_file_path, plugin_name, plugin['method']['default'], channel)
	run_job(job.as_dict(), max_runtime)
	assert os.path.isfile(job.output_file_path)
	os.remove(job.output_file_path)

def prepare_test_files_local(filenames):
	for f in filenames:
		src = os.path.abspath("testdata/" + f)
		dest = os.path.abspath(f)
		shutil.copyfile(src, dest)
