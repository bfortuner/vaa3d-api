import time
import pytest
from bigneuron_app.clients.constants import ECS_JOB_ITEMS_TASK
from bigneuron_app.clients.constants import ECS_JOB_ITEMS_CLUSTER, ECS_JOBS_CLUSTER
from bigneuron_app.clients.constants import ECS_JOB_ITEMS_SERVICE
from bigneuron_app.clients.ecs import ECS


@pytest.fixture(scope="module")
def ecs(request):
	ecs = ECS()
	def fin():
		print ("finalizing %s" % ecs)
	request.addfinalizer(fin)
	return ecs

@pytest.fixture(scope="module")
def cluster(request):
	return ECS_JOB_ITEMS_CLUSTER

@pytest.fixture(scope="module")
def service(request):
	return ECS_JOB_ITEMS_SERVICE

@pytest.fixture(scope="module")
def task(request):
	return ECS_JOB_ITEMS_TASK

def test_get_cluster(ecs, cluster):
	cluster = ecs.get_cluster(cluster)
	print "CLUSTER:\n%s" % str(cluster)
	assert cluster is not None

def test_get_instance_ids_in_cluster(ecs, cluster):
	ids = ecs.get_instance_ids_in_cluster(cluster)
	print "INSTANCE_IDS IN CLUSTER: " + str(ids)
	assert ids is not None

def test_describe_instances(ecs, cluster):
	instance_ids = ecs.get_instance_ids_in_cluster(cluster)
	assert instance_ids is not None
	instances = ecs.describe_instances(cluster, instance_ids)
	print "INSTANCES IN CLUSTER: " + str(instances)
	assert instances is not None

def test_run_task_on_any_instance(ecs, cluster, task):
	resp = ecs.run_task_on_any_instance(cluster, task, 1)
	print resp
	task_arn = resp['tasks'][0]['taskArn']
	print task_arn
	resp = ecs.stop_task(cluster, ecs.get_id_from_arn(task_arn))
	print resp

def test_start_task_on_instances(ecs, cluster, task):
	instance_ids = ['fe1502b3-9fc1-4f7e-bd4d-c5dc45f20125']
	env_vars = [
		{
			'name': 'hey',
			'value': 'brendan'
		}
	] 
	resp = ecs.start_task_on_instances(cluster, 
		task, 
		instance_ids,
		env_vars)
	print resp
	tasks = resp['tasks']
	for task in tasks:
		resp = ecs.stop_task(cluster, ecs.get_id_from_arn(task['taskArn']))
		print "STOPPED:\n" + str(resp)

def test_get_service(ecs, cluster, service):
	service = ecs.get_service(cluster, service)
	assert service is not None

def test_get_service_capacity(ecs, cluster, service):
	capacity = ecs.get_service_capacity(cluster, service)
	print "Capacity is " + str(capacity)

def test_set_service_capacity(ecs, cluster, service):
	initial_capacity = ecs.get_service_capacity(cluster, service)
	resp = ecs.set_service_capacity(cluster, service, initial_capacity+1)
	new_capacity = ecs.get_service_capacity(cluster, service)
	assert new_capacity == initial_capacity+1
	resp = ecs.set_service_capacity(cluster, service, initial_capacity)
	final_capacity = ecs.get_service_capacity(cluster, service)
	assert final_capacity == initial_capacity

def test_get_task_ids_on_instance(ecs, cluster):
	instance_id = "fe1502b3-9fc1-4f7e-bd4d-c5dc45f20125"
	task_ids = ecs.get_task_ids_on_instance(cluster, instance_id)
	print task_ids
	assert task_ids is not None

def test_get_id_from_arn(ecs, cluster):
	arn = "arn:aws:ecs:us-west-2:647215175976:task/9c875823-8c23-4e9e-8950-811d3418aefb"
	task_id = ecs.get_id_from_arn(arn)
	assert task_id == "9c875823-8c23-4e9e-8950-811d3418aefb"

	arn = "arn:aws:ecs:us-west-2:647215175976:container-instance/037e6b29-8cef-4c41-bd9b-606f72c88054"
	task_id = ecs.get_id_from_arn(arn)
	assert task_id == "037e6b29-8cef-4c41-bd9b-606f72c88054"

def test_get_task_count_on_instance(ecs):
	instance_id = "5ae981f8-c8ca-4eca-8579-eaa51cd7797a"
	count = ecs.get_task_count_on_instance(ECS_JOBS_CLUSTER, instance_id)
	print count
	assert count is not None