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