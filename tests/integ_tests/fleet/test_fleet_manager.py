from bigneuron_app.fleet.fleet_manager import *
import pytest

def test_calculate_optimal_job_container_capacity():
	calculate_optimal_job_container_capacity()

def test_calculate_optimal_job_instance_capacity():
	optimal_containers = 5
	expected_instances = int(math.ceil(float(optimal_containers) / JOB_CONTAINERS_PER_INSTANCE))
	instances = calculate_optimal_job_instance_capacity(optimal_containers)
	assert instances == expected_instances
	print "Optimal Instances: " + str(instances)

def test_update_jobs_fleet_capacity():
	update_jobs_fleet_capacity()

def test_calculate_optimal_job_item_container_capacity():
	container_count = calculate_optimal_job_item_container_capacity()

def test_calculate_job_item_containers():
	assert calculate_job_item_containers(5) == 1
	assert calculate_job_item_containers(0) == 0
	assert calculate_job_item_containers(1) == 1
	assert calculate_job_item_containers(6) == 2

def test_calculate_optimal_job_item_instance_capacity():
	optimal_containers = 5
	expected_instances = int(math.ceil(float(optimal_containers) / JOB_ITEM_CONTAINERS_PER_INSTANCE))
	instances = calculate_optimal_job_item_instance_capacity(optimal_containers)
	assert instances == expected_instances
	print "Optimal JobItem Instances: " + str(instances)

def test_update_job_items_fleet_capacity():
	update_job_items_fleet_capacity()

def test_update_job_items_fleet_containers():
	update_job_items_fleet_containers()

def test_get_available_instance_w_most_containers():
	instance_id = get_available_instance_w_most_containers(ECS_JOBS_CLUSTER, JOB_ITEM_CONTAINERS_PER_INSTANCE)
	print "Instance_id: " + str(instance_id)