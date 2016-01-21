import datetime
import time
import math
from bigneuron_app import jobs_log
from bigneuron_app import tasks_log
from bigneuron_app import db
from bigneuron_app.jobs import job_manager
from bigneuron_app.clients import dynamo
from bigneuron_app.clients.constants import SQS_JOB_ITEMS_QUEUE
from bigneuron_app.clients.sqs import sqs
from bigneuron_app.clients.ecs import ecs
from bigneuron_app.clients.autoscaling import autoscaling
from bigneuron_app.clients.constants import ECS_JOBS_CLUSTER, ECS_JOB_ITEMS_CLUSTER
from bigneuron_app.clients.constants import ECS_JOBS_SERVICE, ECS_JOB_ITEMS_SERVICE
from bigneuron_app.clients.constants import ECS_JOBS_TASK, ECS_JOB_ITEMS_TASK
from bigneuron_app.fleet.constants import MIN_JOB_CONTAINERS, MAX_JOB_CONTAINERS
from bigneuron_app.fleet.constants import MIN_JOB_ITEM_CONTAINERS, MAX_JOB_ITEM_CONTAINERS
from bigneuron_app.clients.constants import AUTOSCALING_GROUP_JOBS, AUTOSCALING_GROUP_JOB_ITEMS
from bigneuron_app.fleet.constants import MIN_JOB_INSTANCES, MAX_JOB_INSTANCES
from bigneuron_app.fleet.constants import MIN_JOB_ITEM_INSTANCES, MAX_JOB_ITEM_INSTANCES
from bigneuron_app.fleet.constants import JOB_CONTAINERS_PER_INSTANCE, JOB_ITEM_CONTAINERS_PER_INSTANCE
from bigneuron_app.fleet.constants import NEW_JOB_WAIT_PERIOD_SECONDS
from bigneuron_app.fleet.constants import JOB_ITEMS_PER_CONTAINER


def update_fleet_capacity():
	update_jobs_fleet_capacity()
	update_job_items_fleet_capacity()

def update_jobs_fleet_capacity():
	container_cnt = update_jobs_fleet_containers(ECS_JOBS_CLUSTER, ECS_JOBS_SERVICE, 
		MAX_JOB_CONTAINERS, MIN_JOB_CONTAINERS, NEW_JOB_WAIT_PERIOD_SECONDS)
	instance_cnt = update_jobs_fleet_instances(container_cnt, AUTOSCALING_GROUP_JOBS, 
		MAX_JOB_INSTANCES, MIN_JOB_INSTANCES, JOB_CONTAINERS_PER_INSTANCE)


### Job Containers

def update_jobs_fleet_containers(cluster, service, max_cnts, min_cnts, cooldown):
	current_containers = ecs.get_service_capacity(cluster, service)
	optimal_containers = calculate_optimal_job_container_capacity(cooldown)
	tasks_log.info("JobsContainers - Current:%s Optimal:%s" % (str(current_containers), str(optimal_containers)))
	if optimal_containers > current_containers and current_containers < max_cnts:
		tasks_log.info("Jobs - Increasing Container Capacity")
		ecs.set_service_capacity(cluster, service, current_containers+1)
		return current_containers+1
	elif optimal_containers < current_containers and current_containers > min_cnts:
		tasks_log.info("Jobs - Reducing Container Capacity")
		ecs.set_service_capacity(cluster, service, current_containers-1)
		return current_containers-1
	else:
		tasks_log.info("Jobs - Leaving Container Capacity Unchanged")
		return current_containers

def calculate_optimal_job_container_capacity(cooldown):
	seconds_since_last_job = get_seconds_since_last_job_run(cooldown)
	jobs_in_flight = (len(job_manager.get_jobs_by_status("IN_PROGRESS")) + 
		len(job_manager.get_jobs_by_status("CREATED")))
	msg = ("SITUATION:\nSecondsSinceLastJobRun: %s\nJobCount: %s")
	msg = msg % (seconds_since_last_job, jobs_in_flight)
	tasks_log.info(msg)
	if jobs_in_flight == 0:
		tasks_log.info("no jobs in flight")
		if seconds_since_last_job > cooldown:
			return 0
		else:
			return 1
	else:
		tasks_log.info("found jobs in flight")
		return 1

def get_seconds_since_last_job_run(cooldown):
	current_time = datetime.datetime.utcnow()
	last_updated_job_time = job_manager.get_last_updated_job().last_updated
	#Handle case where this is the first job 
	if not last_updated_job_time:
		return cooldown+1
	return int((current_time - last_updated_job_time).total_seconds())	


### Job Instances

def update_jobs_fleet_instances(optimal_cnts, autoscaling_group, max_inst, min_inst, cnts_per_inst):
	current_instances = autoscaling.get_capacity(autoscaling_group)
	optimal_instances = calculate_optimal_job_instance_capacity(optimal_cnts, cnts_per_inst)
	tasks_log.info("JobsInstances - Current:%s Optimal:%s" % (str(current_instances), str(optimal_instances)))
	if optimal_instances > current_instances and current_instances < max_inst:
		tasks_log.info("Jobs - Increasing Instance Capacity")
		autoscaling.increase_capacity(autoscaling_group)
		return current_instances+1
	elif optimal_instances < current_instances and current_instances > min_inst:
		tasks_log.info("Jobs - Reducing Instance Capacity")
		autoscaling.decrease_capacity(autoscaling_group)
		return current_instances-1
	else:
		tasks_log.info("Jobs - Leaving Instance Capacity Unchanged")
		return current_instances

def calculate_optimal_job_instance_capacity(opt_cntrs, cntrs_per_inst):
	instances = int(math.ceil(float(opt_cntrs) / cntrs_per_inst))
	return instances


### JobItem Containers

def update_job_items_fleet_capacity():
	cntr_cnt = update_job_items_fleet_containers(ECS_JOB_ITEMS_CLUSTER, SQS_JOB_ITEMS_QUEUE, 
		MAX_JOB_ITEM_CONTAINERS, MIN_JOB_ITEM_CONTAINERS, JOB_ITEMS_PER_CONTAINER)
	inst_cnt = update_job_items_fleet_instances(AUTOSCALING_GROUP_JOB_ITEMS, MAX_JOB_ITEM_INSTANCES, 
		MIN_JOB_ITEM_INSTANCES, JOB_ITEM_CONTAINERS_PER_INSTANCE, cntr_cnt)

def update_job_items_fleet_containers(cluster, queue, max_cntrs, min_cntrs, itms_per_cntr):
	"""
	Slow scale up. No scale down (tasks will die after they complete)
	"""
	current_containers = ecs.get_total_tasks_in_cluster(cluster)
	optimal_containers = calculate_optimal_job_item_container_capacity(queue, itms_per_cntr)
	tasks_log.info("JobItemsContainers - Current:%s Optimal:%s" % (str(current_containers), 
		str(optimal_containers)))
	if optimal_containers > current_containers and current_containers < max_cntrs:
		tasks_log.info("JobItems - Increasing Container Capacity")
		add_job_item_containers(current_containers+1)
		return optimal_containers
	elif optimal_containers < current_containers and current_containers > min_cntrs:
		tasks_log.info("JobItems - Reducing Container Capacity")
		remove_job_item_containers(current_containers-1)
		return current_containers-1
	else:
		tasks_log.info("JobItems - Leaving Container Capacity Unchanged")
		return optimal_containers

def calculate_optimal_job_item_container_capacity(queue, itms_per_cntr):
	"""
	Checks size of JobItems queue and compares with constant JOB_ITEMS_PER_CONTAINER
	"""
	current_time = datetime.datetime.utcnow()
	last_updated_job_item_time = datetime.datetime.utcnow() #job_manager.get_last_updated_job().last_updated
	seconds_since_last_job_item = int((current_time - last_updated_job_item_time).total_seconds())
	
	job_items_queue = sqs.get_queue(queue)
	queue_size = sqs.get_queue_size(job_items_queue.url)
	optimal_containers = calculate_job_item_containers(queue_size, itms_per_cntr)
	msg = ("SITUATION:\nCurrentTime: %s\nLast_Updated: %s\nSecondsSinceLastUpdate: " + 
		"%s\nJobItemQueueSize: %s\nOptimalContainers: %s")
	msg = msg % (current_time, last_updated_job_item_time, seconds_since_last_job_item, 
		queue_size, optimal_containers)
	tasks_log.info(msg)
	return optimal_containers

def calculate_job_item_containers(queue_size, itms_per_cntr):	
	#5.0 / 5 = 1
	#1.0 / 5 = .2 = 1
	return int(math.ceil(float(queue_size) / itms_per_cntr))

def get_available_instance_w_most_containers(cluster, max_containers):
	"""
	JOB_ITEM_CONTAINERS_PER_INSTANCE
	Place the container on the instance that's nearly full
	This way less-active instances will free-up more frequently
	"""
	instance_ids = ecs.get_instance_ids_in_cluster(cluster)
	if len(instance_ids) == 0:
		return None
	max_count = 0
	max_instance_id = None
	for instance_id in instance_ids:
		count = ecs.get_task_count_on_instance(cluster, instance_id)
		if count >= max_containers:
			pass
		elif count >= max_count:
			max_count = count
			max_instance_id = instance_id
	return max_instance_id

def add_job_item_containers(count):
	"""
	Add to instance with most containers
	"""
	i = 0;
	while i < count:
		instance_id = get_available_instance_w_most_containers(ECS_JOB_ITEMS_CLUSTER, 
			JOB_ITEM_CONTAINERS_PER_INSTANCE)
		if instance_id:
			tasks_log.info("JobItem - Adding Container To Instance " + instance_id)
			ecs.start_task_on_instance(ECS_JOB_ITEMS_CLUSTER, ECS_JOB_ITEMS_TASK, instance_id)
		else:
			tasks_log.info("Attempt To Add Container Failed. No available instances found.")
		time.sleep(2)
		i+=1

def remove_job_item_containers(count):
	"""
	Remove from least full instance
	Currently do nothing - we will let tasks expire on their own
	"""
	pass


### Job Item Instances

def update_job_items_fleet_instances(autoscaling_grp, max_insts, min_insts, cntrs_per_inst, cntrs):
	"""
	Fast scale up. Slow scale down.
	"""
	current_instances = autoscaling.get_capacity(autoscaling_grp)
	optimal_instances = calculate_optimal_job_item_instance_capacity(cntrs_per_inst, cntrs)
	tasks_log.info("JobItemsInstances: Current:%s Optimal:%s" % (str(current_instances), 
		str(optimal_instances)))
	if optimal_instances > current_instances and current_instances < max_insts:
		tasks_log.info("JobItems - Increasing Instance Capacity")
		autoscaling.increase_capacity(autoscaling_grp)
		return current_instances+1
	elif optimal_instances < current_instances and current_instances > min_insts:
		tasks_log.info("JobItems - Reducing Instance Capacity")
		autoscaling.decrease_capacity(autoscaling_grp)
		return current_instances-1
	else:
		tasks_log.info("JobItems - Leaving Instance Capacity Unchanged")
		return current_instances

def calculate_optimal_job_item_instance_capacity(cntrs_per_inst, opt_cntrs):
	optimal_instances = int(math.ceil(float(opt_cntrs) / cntrs_per_inst))
	msg = "SITUATION:\nOptimalJobItemContainers: %s\nJobItemContainerPerInstance: %s\nOptimalJobItemInstances: %s"
	msg = msg % (opt_cntrs, cntrs_per_inst, optimal_instances)
	tasks_log.info(msg)
	return optimal_instances

