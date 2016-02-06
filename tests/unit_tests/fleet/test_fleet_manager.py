import os
import mock
from pytest_mock import mocker 
from bigneuron_app.fleet import fleet_manager
from bigneuron_app.fleet import constants
from bigneuron_app.utils import mockexample
from bigneuron_app import config
import pytest


def test_update_fleet_capacity(mocker):
	mocker.patch.object(fleet_manager, 'update_jobs_fleet_capacity')
	mocker.patch.object(fleet_manager, 'update_job_items_fleet_capacity')

	fleet_manager.update_fleet_capacity()
	
	fleet_manager.update_jobs_fleet_capacity.assert_called_with()
	fleet_manager.update_job_items_fleet_capacity.assert_called_with()

def test_update_jobs_fleet_capacity(mocker, monkeypatch):
	mocker.patch.object(fleet_manager, 'update_jobs_fleet_containers')
	mocker.patch.object(fleet_manager, 'update_jobs_fleet_instances')
	monkeypatch.setattr(fleet_manager, 'MAX_JOB_INSTANCES', 1)
	monkeypatch.setattr(fleet_manager, 'MIN_JOB_INSTANCES', 0)

	fleet_manager.update_jobs_fleet_containers.return_value = 5

	fleet_manager.update_jobs_fleet_capacity()
	
	fleet_manager.update_jobs_fleet_containers.assert_called_with('vaa3d-jobs-test', 'vaa3d-jobs', 1, 0, 120)
	fleet_manager.update_jobs_fleet_instances.assert_called_with(5, 'Vaa3d-Jobs-Test-Autoscaling', 1, 0, 2)

def test_update_jobs_fleet_containers__increase(mocker):
	max_cnts = 3
	min_cnts = 0
	mocker.patch.object(fleet_manager, 'ecs')
	mocker.patch.object(fleet_manager, 'calculate_optimal_job_container_capacity')
	
	fleet_manager.ecs.get_service_capacity.return_value = 0
	fleet_manager.calculate_optimal_job_container_capacity.return_value = 2

	fleet_manager.update_jobs_fleet_containers('TestCluster', 'TestService', max_cnts, min_cnts, 30)
	
	fleet_manager.ecs.set_service_capacity.assert_called_with('TestCluster', 'TestService', 1)

def test_update_jobs_fleet_containers__increase_over_max(mocker):
	max_cnts = 2
	min_cnts = 0
	mocker.patch.object(fleet_manager, 'ecs')
	mocker.patch.object(fleet_manager, 'calculate_optimal_job_container_capacity')

	fleet_manager.ecs.get_service_capacity.return_value = 2
	fleet_manager.calculate_optimal_job_container_capacity.return_value = 3

	fleet_manager.update_jobs_fleet_containers('TestCluster', 'TestService', max_cnts, 
		min_cnts, mock.ANY)

	fleet_manager.ecs.set_service_capacity.assert_not_called()

def test_update_jobs_fleet_containers__decrease_under_min(mocker):
	max_cnts = 2
	min_cnts = 1
	mocker.patch.object(fleet_manager, 'ecs')
	mocker.patch.object(fleet_manager, 'calculate_optimal_job_container_capacity')

	fleet_manager.ecs.get_service_capacity.return_value = 1
	fleet_manager.calculate_optimal_job_container_capacity.return_value = 0

	fleet_manager.update_jobs_fleet_containers('TestCluster', 'TestService', max_cnts, 
		min_cnts, mock.ANY)

	fleet_manager.ecs.set_service_capacity.assert_not_called()

@pytest.mark.parametrize('test_type, cur_cnts, opt_cnts, expected', [
	('optimal_greater_than_max_returns_max', 2, 3, 2),
	('optimal_less_than_current_and_current_equals_min_return_min', 1, 0, 1),
 	('optimal_equals_current_return_current', 2, 2, 2),
	('optimal_less_than_current_return_current_minus_one', 2, 1, 1),
	('optimal_less_than_current_return_current_minus_one', 2, 0, 1)
])
def test_update_jobs_fleet_containers(mocker, test_type, cur_cnts, opt_cnts, expected):
	max_cnts = 2
	min_cnts = 1
	mocker.patch.object(fleet_manager, 'ecs')
	mocker.patch.object(fleet_manager, 'calculate_optimal_job_container_capacity')

	fleet_manager.ecs.get_service_capacity.return_value = cur_cnts
	fleet_manager.calculate_optimal_job_container_capacity.return_value = opt_cnts

	assert fleet_manager.update_jobs_fleet_containers('TestCluster', 'TestService', max_cnts, 
		min_cnts, mock.ANY) == expected

@pytest.mark.parametrize('test_type, cur_inst, opt_inst, expected', [
	('optimal_greater_than_max_returns_max', 2, 3, 2),
	('optimal_less_than_current_and_current_equals_min_return_min', 1, 1, 1),
	('optimal_equals_current_return_current', 2, 2, 2),
	('optimal_less_than_current_return_current_minus_one', 2, 1, 1),
	('optimal_less_than_current_return_current_minus_one', 2, 0, 1),
])
def test_update_jobs_fleet_instances(mocker, test_type, cur_inst, opt_inst, expected):
	max_inst = 2
	min_inst = 1
	mocker.patch.object(fleet_manager, 'autoscaling')
	mocker.patch.object(fleet_manager, 'calculate_optimal_job_instance_capacity')

	fleet_manager.autoscaling.get_capacity.return_value = cur_inst
	fleet_manager.calculate_optimal_job_instance_capacity.return_value = opt_inst

	assert fleet_manager.update_jobs_fleet_instances(mock.ANY, 'TestService', max_inst, 
		min_inst, mock.ANY) == expected

@pytest.mark.parametrize('test_type, jobs, sec_since_last, cooldown, expected', [
	('no_jobs_and_last_job_time_greater_than_cooldown_return_0', [], 100, 30, 0),
	('no_jobs_and_last_job_time_less_than_cooldown_return_1', [], 20, 30, 1),
	('more_than_one_job_return_1', ['Job'], 20, 30, 1),
])
def test_calculate_optimal_job_container_capacity(mocker, test_type, jobs, sec_since_last, 
	cooldown, expected):
	mocker.patch.object(fleet_manager, 'get_seconds_since_last_job_run')
	mocker.patch.object(fleet_manager, 'job_manager')

	fleet_manager.get_seconds_since_last_job_run.return_value = sec_since_last
	fleet_manager.job_manager.get_jobs_by_status.return_value = jobs

	assert fleet_manager.calculate_optimal_job_container_capacity(cooldown) == expected

@pytest.mark.parametrize('opt_cnts, cnts_per_inst, expected', [
	(5, 2, 3),
	(4, 2, 2),
	(0, 2, 0),
])
def test_calculate_optimal_job_instance_capacity(opt_cnts, cnts_per_inst, expected):
	assert fleet_manager.calculate_optimal_job_instance_capacity(opt_cnts, 
		cnts_per_inst) == expected

def test_update_job_items_fleet_capacity__containers(mocker, monkeypatch):
	monkeypatch.setattr(fleet_manager, 'ECS_JOB_ITEMS_CLUSTER', 'TestCluster')
	monkeypatch.setattr(fleet_manager, 'SQS_JOB_ITEMS_QUEUE', 'TestJobItemsQueue')
	monkeypatch.setattr(fleet_manager, 'MAX_JOB_ITEM_CONTAINERS', 6)
	monkeypatch.setattr(fleet_manager, 'MIN_JOB_ITEM_CONTAINERS', 0)
	monkeypatch.setattr(fleet_manager, 'JOB_ITEMS_PER_CONTAINER', 2)
	mocker.patch.object(fleet_manager, 'autoscaling')
	mocker.patch.object(fleet_manager, 'ecs')
	mocker.patch.object(fleet_manager, 'update_job_items_fleet_containers')

	fleet_manager.update_job_items_fleet_containers.return_value = 5

	fleet_manager.update_job_items_fleet_capacity()
	
	fleet_manager.update_job_items_fleet_containers.assert_called_with('TestCluster', 
		'TestJobItemsQueue', 6, 0, 2)

def test_update_job_items_fleet_capacity__instances(mocker, monkeypatch):
	mocker.patch.object(fleet_manager, 'update_job_items_fleet_containers')
	mocker.patch.object(fleet_manager, 'update_job_items_fleet_instances')
	mocker.patch.object(fleet_manager, 'autoscaling', autospec=True)
	mocker.patch.object(fleet_manager, 'ecs', autospec=True)
	monkeypatch.setattr(fleet_manager, 'AUTOSCALING_GROUP_JOB_ITEMS', 'TestGroup')
	monkeypatch.setattr(fleet_manager, 'MAX_JOB_ITEM_INSTANCES', 3)
	monkeypatch.setattr(fleet_manager, 'MIN_JOB_ITEM_INSTANCES', 0)
	monkeypatch.setattr(fleet_manager, 'JOB_ITEM_CONTAINERS_PER_INSTANCE', 2)

	fleet_manager.update_job_items_fleet_containers.return_value = 3

	fleet_manager.update_job_items_fleet_capacity()
	
	fleet_manager.update_job_items_fleet_instances.assert_called_with('TestGroup', 
		3, 0, 2, 3)

def test_update_job_items_fleet_containers__increase(mocker):
	max_cntrs = 6
	min_cntrs = 0
	cur_cntrs = 1
	opt_cntrs = 3
	mocker.patch.object(fleet_manager, 'ecs')
	mocker.patch.object(fleet_manager, 'calculate_optimal_job_item_container_capacity')
	mocker.patch.object(fleet_manager, 'add_job_item_containers')

	fleet_manager.ecs.get_total_tasks_in_cluster.return_value = cur_cntrs
	fleet_manager.calculate_optimal_job_item_container_capacity.return_value = opt_cntrs

	result = fleet_manager.update_job_items_fleet_containers('TestCluster', 'TestQueue', max_cntrs, 
		min_cntrs, mock.ANY)
	assert result == opt_cntrs
	fleet_manager.add_job_item_containers.assert_called_with(cur_cntrs+1)

def test_update_job_items_fleet_containers__decrease(mocker):
	max_cntrs = 6
	min_cntrs = 0
	cur_cntrs = 2
	opt_cntrs = 0
	mocker.patch.object(fleet_manager, 'ecs')
	mocker.patch.object(fleet_manager, 'calculate_optimal_job_item_container_capacity')
	mocker.patch.object(fleet_manager, 'remove_job_item_containers')

	fleet_manager.ecs.get_total_tasks_in_cluster.return_value = cur_cntrs
	fleet_manager.calculate_optimal_job_item_container_capacity.return_value = opt_cntrs

	result = fleet_manager.update_job_items_fleet_containers('TestCluster', 'TestQueue', max_cntrs, 
		min_cntrs, 99)
	assert result == cur_cntrs-1
	fleet_manager.remove_job_item_containers.assert_called_with(cur_cntrs-1)

def test_update_job_items_fleet_containers__unchanged(mocker):
	max_cntrs = 6
	min_cntrs = 0
	cur_cntrs = 1
	opt_cntrs = 1
	mocker.patch.object(fleet_manager, 'ecs')
	mocker.patch.object(fleet_manager, 'calculate_optimal_job_item_container_capacity')
	mocker.patch.object(fleet_manager, 'add_job_item_containers')
	mocker.patch.object(fleet_manager, 'remove_job_item_containers')

	fleet_manager.ecs.get_total_tasks_in_cluster.return_value = cur_cntrs
	fleet_manager.calculate_optimal_job_item_container_capacity.return_value = opt_cntrs

	result = fleet_manager.update_job_items_fleet_containers('TestCluster', 'TestQueue', max_cntrs, 
		min_cntrs, mock.ANY)
	assert result == opt_cntrs
	fleet_manager.add_job_item_containers.assert_not_called()
	fleet_manager.remove_job_item_containers.assert_not_called()

@pytest.mark.parametrize('test_type, cur_cntrs, opt_cntrs, expected', [
	('optimal_greater_than_max_returns_optimal', 2, 3, 3),
	('optimal_greater_than_current_under_max_returns_optimal', 0, 2, 2),
 	('optimal_equals_current_return_current', 2, 2, 2),
	('optimal_less_than_min_and_current_equals_min_return_optimal', 1, 0, 0),
	('optimal_less_than_current_return_current_minus_one', 2, 1, 1),
	('optimal_less_than_current_return_current_minus_one', 2, 0, 1)
])
def test_update_job_items_fleet_containers(mocker, test_type, cur_cntrs, opt_cntrs, expected):
	max_cntrs = 2
	min_cntrs = 1
	mocker.patch.object(fleet_manager, 'ecs')
	mocker.patch.object(fleet_manager, 'sqs')
	mocker.patch.object(fleet_manager, 'calculate_optimal_job_item_container_capacity')

	fleet_manager.ecs.get_total_tasks_in_cluster.return_value = cur_cntrs
	fleet_manager.calculate_optimal_job_item_container_capacity.return_value = opt_cntrs

	result = fleet_manager.update_job_items_fleet_containers('TestCluster', 'TestQueue', max_cntrs, 
		min_cntrs, mock.ANY)
	assert result == expected

def test_calculate_optimal_job_item_container_capacity(mocker):
	queue_size = 10
	itms_per_cntr = 5
	mocker.patch.object(fleet_manager, 'sqs')
	mocker.patch.object(fleet_manager, 'calculate_job_item_containers')
	
	fleet_manager.sqs.get_queue_size.return_value = queue_size

	fleet_manager.calculate_optimal_job_item_container_capacity('TestQueue', itms_per_cntr)

	fleet_manager.calculate_job_item_containers.assert_called_with(queue_size, itms_per_cntr)

@pytest.mark.parametrize('queue_size, itms_per_cntr, expected', [
	(10, 5, 2),
	(10, 4, 3),
	(0, 4, 0),
	(1, 4, 1),
])
def test_calculate_job_item_containers(queue_size, itms_per_cntr, expected):
	result = fleet_manager.calculate_job_item_containers(queue_size, itms_per_cntr)
	assert result == expected

@pytest.mark.parametrize('test_type, instances, task_counts, max_cntrs, expected', [
	('max_instance_at_begin', ['A','B','C'], [5,3,1], 10, 'A'),
	('max_instance_in_middle', ['A','B','C'], [1,5,3], 10, 'B'),
	('max_instance_at_end', ['A','B','C'], [1,3,5], 10, 'C'),
	('max_instance_already_full', ['A','B','C'], [10,5,3], 10, 'B'),
	('all_instance_empty', ['A','B','C'], [0,0,0], 10, 'C'),
	('no_instances', [], [], 10, None),
])
def test_get_available_instance_w_most_containers(mocker, test_type, instances, task_counts, max_cntrs, expected):
	fleet_manager.ecs.get_instance_ids_in_cluster = mock.MagicMock(return_value=instances)
	fleet_manager.ecs.get_task_count_on_instance = mock.MagicMock(side_effect=task_counts)
	result = fleet_manager.get_available_instance_w_most_containers('TestCluster', max_cntrs)
	assert result == expected

def test_add_job_item_containers(mocker, monkeypatch):
	monkeypatch.setattr(fleet_manager, 'ECS_JOB_ITEMS_CLUSTER', 'TestCluster')
	monkeypatch.setattr(fleet_manager, 'ECS_JOB_ITEMS_TASK', 'TestJobItemsTask')
	mocker.patch.object(fleet_manager, 'ecs')
	mocker.patch.object(fleet_manager, 'get_available_instance_w_most_containers')
	#This type of mock is module-wide. Use patch instead.
	#fleet_manager.get_available_instance_w_most_containers = mock.MagicMock(
	#	side_effect=['A','A','B',None])
	#This type of mock cleans itself up so is preferable
	fleet_manager.get_available_instance_w_most_containers.side_effect = ['A','A','B',None]

	fleet_manager.add_job_item_containers(4)

	assert fleet_manager.ecs.start_task_on_instance.call_count == 3

def test_remove_job_item_containers():
	assert True

@pytest.mark.parametrize('test_type, cur_insts, opt_insts, expected', [
	('optimal_equal_current_greater_than_max_return_max', 3, 4, 3),
	('optimal_greater_than_current_under_max_return_current_plus_one', 1, 3, 2),
	('optimal_greater_than_current_under_max_return_current_plus_one', 1, 2, 2),
 	('optimal_equals_current_return_current', 2, 2, 2),
	('optimal_less_than_min_and_current_equals_min_return_min', 0, 0, 0),
	('optimal_less_than_current_return_current_minus_one', 2, 1, 1),
	('optimal_less_than_current_return_current_minus_one', 2, 0, 1)
])
def test_update_job_items_fleet_instances(mocker, test_type, cur_insts, opt_insts, expected):
	max_insts = 3
	min_insts = 0
	mocker.patch.object(fleet_manager, 'autoscaling', autospec=True)
	fleet_manager.autoscaling.get_capacity.return_value = cur_insts
	mocker.patch.object(fleet_manager, 'calculate_optimal_job_item_instance_capacity')
	fleet_manager.calculate_optimal_job_item_instance_capacity.return_value = opt_insts

	result = fleet_manager.update_job_items_fleet_instances('TestAutoGroup', max_insts, 
		min_insts, mock.ANY, mock.ANY)

	assert result == expected

@pytest.mark.parametrize('opt_cntrs, cntrs_per_inst, expected', [
	(4, 2, 2),
	(5, 2, 3),
	(0, 2, 0),
	(1, 2, 1),
])
def test_calculate_optimal_job_item_instance_capacity(opt_cntrs, cntrs_per_inst, expected):
	result = fleet_manager.calculate_optimal_job_item_instance_capacity(cntrs_per_inst, opt_cntrs)
	assert result == expected





## Examples

def test_mocker_example_pytest_raises_exception(mocker):
	mocker.patch.object(mockexample, 'method_which_doesnt_usually_throw_exception')
	mockexample.method_which_doesnt_usually_throw_exception.side_effect = Exception()
	with pytest.raises(Exception):
		mockexample.method_which_doesnt_usually_throw_exception()

def test_pytest_monkeypatch__set_env_variable(monkeypatch):
	monkeypatch.setenv('VAA3D_CONFIG', 'FakeConfig')
	assert mockexample.method_which_uses_env_variable() == 'FakeConfig'

