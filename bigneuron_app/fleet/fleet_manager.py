import datetime
import time
import math
from bigneuron_app import jobs_log
from bigneuron_app import tasks_log
from bigneuron_app import db
from bigneuron_app.jobs import job_manager
from bigneuron_app.clients import dynamo
from bigneuron_app.clients.sqs import SQS
from bigneuron_app.clients.ecs import ECS
from bigneuron_app.clients.constants import ECS_JOBS_CLUSTER, ECS_JOB_ITEMS_CLUSTER
from bigneuron_app.clients.constants import ECS_JOBS_SERVICE, ECS_JOB_ITEMS_SERVICE
from bigneuron_app.fleet.constants import MIN_JOB_CONTAINERS, MAX_JOB_CONTAINERS
from bigneuron_app.fleet.constants import MIN_JOB_ITEM_CONTAINERS, MAX_JOB_ITEM_CONTAINERS
from bigneuron_app.clients.autoscaling import Autoscaling
from bigneuron_app.clients.constants import AUTOSCALING_GROUP_JOBS, AUTOSCALING_GROUP_JOB_ITEMS
from bigneuron_app.fleet.constants import MIN_JOB_INSTANCES, MAX_JOB_INSTANCES
from bigneuron_app.fleet.constants import MIN_JOB_ITEM_INSTANCES, MAX_JOB_ITEM_INSTANCES
from bigneuron_app.fleet.constants import JOB_CONTAINERS_PER_INSTANCE
from bigneuron_app.fleet.constants import NEW_JOB_WAIT_PERIOD_SECONDS

sqs = SQS()
ecs = ECS()
autoscaling = Autoscaling()

def update_fleet():
	update_jobs_fleet_capacity()
	update_job_items_fleet_capacity()

def update_jobs_fleet_capacity():
	current_containers = ecs.get_service_capacity(ECS_JOBS_CLUSTER, ECS_JOBS_SERVICE)
	optimal_containers = calculate_optimal_job_container_capacity()
	print "Jobs - Containers: " + str(current_containers) + " " + str(optimal_containers)
	if optimal_containers > current_containers and current_containers < MAX_JOB_CONTAINERS:
		tasks_log.info("Jobs - Increasing Container Capacity")
		ecs.set_service_capacity(ECS_JOBS_CLUSTER, ECS_JOBS_SERVICE, current_containers+1)
	elif optimal_containers < current_containers and current_containers > MIN_JOB_CONTAINERS:
		tasks_log.info("Jobs - Reducing Container Capacity")
		ecs.set_service_capacity(ECS_JOBS_CLUSTER, ECS_JOBS_SERVICE, current_containers-1)
	else:
		tasks_log.info("Jobs - Container Capacity Unchanged")

	current_instances = autoscaling.get_capacity(AUTOSCALING_GROUP_JOBS)
	optimal_instances = calculate_optimal_job_instance_capacity(optimal_containers)
	print "Jobs - Instances: " + str(current_instances) + " " + str(optimal_instances)
	if optimal_instances > current_instances and current_instances < MAX_JOB_INSTANCES:
		tasks_log.info("Jobs - Increasing Instance Capacity")
		autoscaling.increase_capacity(AUTOSCALING_GROUP_JOBS)
	elif optimal_instances < current_instances and current_instances > MIN_JOB_INSTANCES:
		tasks_log.info("Jobs - Reducing Instance Capacity")
		autoscaling.decrease_capacity(AUTOSCALING_GROUP_JOBS)
	else:
		tasks_log.info("Jobs - Instance Capacity Unchanged")

def calculate_optimal_job_container_capacity():
	current_time = datetime.datetime.utcnow()
	last_updated_job_time = job_manager.get_last_updated_job().last_updated
	seconds_since_last_job = int((current_time - last_updated_job_time).total_seconds())
	jobs_in_flight = (len(job_manager.get_jobs_by_status("IN_PROGRESS")) + 
		len(job_manager.get_jobs_by_status("CREATED")))
	msg = ("SITUATION:\nCurrentTime: %s\nLast_Updated: %s\nSecondsSinceLastUpdate: %s\nJobCount: %s")
	msg = msg % (current_time, last_updated_job_time, seconds_since_last_job, jobs_in_flight)
	print msg
	if jobs_in_flight == 0:
		print "no jobs in flight"
		if seconds_since_last_job > NEW_JOB_WAIT_PERIOD_SECONDS:
			return 0
		else:
			return 1
	else:
		print "found jobs in flight"
		return 1

def calculate_optimal_job_instance_capacity(optimal_containers):
	instances = int(math.ceil(float(optimal_containers) / JOB_CONTAINERS_PER_INSTANCE))
	return instances

def update_job_items_fleet_capacity():
	pass

