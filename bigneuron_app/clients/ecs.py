import boto3
import json
import time
from bigneuron_app.clients.constants import *
from bigneuron_app import items_log


class ECS:
	def __init__(self):
		self.client = None

	def get_client(self):
		if self.client:
			return self.client
		return boto3.client('ecs', region_name=AWS_REGION, 
			aws_access_key_id=AWS_ACCESS_KEY, 
			aws_secret_access_key=AWS_SECRET_KEY)

	def start_task_on_instances(self, cluster, task_name, instance_ids, env_vars):
		#Start task on the specified container instance w ENV/CMD overrides
		#boto3.readthedocs.org/en/latest/reference/services/ecs.html#ECS.Client.start_task
		response = self.get_client().start_task(
			cluster=cluster,
			taskDefinition=task_name,
			overrides={
				'containerOverrides': [
					{
						'name': task_name,
						# 'command': [
						# 	'string',
						# ],
						'environment': env_vars
					},
				]
			},
			containerInstances=instance_ids,
			startedBy='vaa3d_worker'
		)
		return response

	def run_task_on_any_instance(self, cluster, task_name, count, overrides={}):
		#Start a task using random placement and the default Amazon ECS scheduler
		#boto3.readthedocs.org/en/latest/reference/services/ecs.html#ECS.Client.run_task
		response = self.get_client().run_task(
			cluster=cluster,
			taskDefinition=task_name,
			overrides=overrides,
			count=count,
			startedBy='vaa3d_api'
		)
		return response

	def stop_task(self, cluster, task_id):
		#boto3.readthedocs.org/en/latest/reference/services/ecs.html#ECS.Client.stop_task
		response = self.get_client().stop_task(
			cluster=cluster,
			task=task_id,
			reason='COMPLETE'
		)
		return response

	def update_service(self, cluster, service, count, task):
		response = client.update_service(
			cluster=cluster,
			service=service,
			desiredCount=count,
			taskDefinition=task #task:version
		)
		return response

	def get_instance_ids_in_cluster(self, cluster):
		#returns list of ARNs
		#boto3.readthedocs.org/en/latest/reference/services/ecs.html#ECS.Client.list_container_instances
		response = self.get_client().list_container_instances(
			cluster=cluster
		)
		ids = []
		for arn in response['containerInstanceArns']:
			ids.append(self.get_id_from_arn(arn))
		return ids

	def describe_instances(self, cluster, instance_ids):
		#Returns ec2_instance_id and other metadata given list of ARNs or Ids
		#boto3.readthedocs.org/en/latest/reference/services/ecs.html#ECS.Client.describe_container_instances
		response = self.get_client().describe_container_instances(
			cluster=cluster,
			containerInstances=instance_ids
		)
		return response['containerInstances']

	def get_tasks_by_id(self, cluster, task_ids):
		#boto3.readthedocs.org/en/latest/reference/services/ecs.html#ECS.Client.describe_tasks
		response = self.get_client().describe_tasks(
			cluster=cluster,
			tasks=task_ids
		)
		return response

	def get_task_ids_on_instance(self, cluster, instance_id, status='RUNNING'):
		#boto3.readthedocs.org/en/latest/reference/services/ecs.html#ECS.Client.list_tasks
		#maybe let the client call this directly w params they want
		response = self.get_client().list_tasks(
			cluster=cluster,
			containerInstance=instance_id,
			desiredStatus=status #'RUNNING'|'PENDING'|'STOPPED'
		)
		ids = []
		for arn in response['taskArns']:
			ids.append(self.get_id_from_arn(arn))
		return ids

	def get_id_from_arn(self, arn):
		return arn[arn.find("/")+1:]

