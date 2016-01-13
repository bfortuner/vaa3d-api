import time
import pytest
from bigneuron_app.clients.constants import AUTOSCALING_GROUP_JOBS
from bigneuron_app.clients.autoscaling import Autoscaling


@pytest.fixture(scope="module")
def autoscaling(request):
	autoscaling = Autoscaling()
	def fin():
		print ("finalizing %s" % autoscaling)
	request.addfinalizer(fin)
	return autoscaling

@pytest.fixture(scope="module")
def group():
	return AUTOSCALING_GROUP_JOBS

def test_get_autoscaling_group(autoscaling, group):
	resp = autoscaling.get_autoscaling_group(group)
	print "Autoscaling Group"
	print resp
	assert resp is not None

@pytest.mark.skipif(True, reason="Too slow")
def test_increase_capacity(autoscaling, group):
	initial_capacity = autoscaling.get_capacity(group)
	autoscaling.increase_capacity(group)
	result = wait_for_capacity_change(autoscaling, group, initial_capacity+1)
	assert result is True

@pytest.mark.skipif(True, reason="Too slow. Conflicts with increase capacity")
def test_decrease_capacity(autoscaling, group):
	initial_capacity = autoscaling.get_capacity(group)
	autoscaling.decrease_capacity(group)
	result = wait_for_capacity_change(autoscaling, group, initial_capacity-1)
	assert result is True

def test_list_scheduled_activities(autoscaling, group):
	activities = autoscaling.list_scheduled_activities(group)
	assert activities is not None

def test_list_scaling_activities(autoscaling, group):
	activities = autoscaling.list_scaling_activities(group)
	assert activities is not None

def test_remove_instance(autoscaling, group):
	instances = autoscaling.get_instances(group)
	print "current instances: " + str(instances)
	for instance in instances:
		instance_id = instance['InstanceId']
		resp = autoscaling.remove_instance(instance_id)
		print "removed instance_id: " + str(instance_id) + str(resp)


# Helpers
def wait_for_capacity_change(autoscaling, group, expected):
	sleep_time=5
	max_attempts=10
	attempt=0
	while attempt < max_attempts:
		print "waiting for capacity change"
		group_info = autoscaling.get_autoscaling_group(group)
		instance_count = len(group_info['Instances'])
		if instance_count == expected:
			return True
		attempt+=1
		time.sleep(sleep_time)  
	return False