import boto3
import json
import time
from datetime import datetime
from bigneuron_app.clients.constants import *


class Autoscaling:
	def __init__(self):
		self.client = None

	def get_client(self):
		if self.client:
			return self.client
		return boto3.client('autoscaling', region_name=AWS_REGION, 
			aws_access_key_id=AWS_ACCESS_KEY, 
			aws_secret_access_key=AWS_SECRET_KEY)

	def get_autoscaling_group(self, autoscaling_group):
		#boto3.readthedocs.org/en/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_auto_scaling_groups
		response = self.get_client().describe_auto_scaling_groups(
			AutoScalingGroupNames=[autoscaling_group]
		)
		return response['AutoScalingGroups'][0]

	def increase_capacity(self, autoscaling_group):
		capacity = self.get_capacity(autoscaling_group)
		self.set_capacity(autoscaling_group, capacity+1)

	def decrease_capacity(self, autoscaling_group):
		capacity = self.get_capacity(autoscaling_group)
		self.set_capacity(autoscaling_group, capacity-1)

	def remove_instance(self, instance_id, reduce_capacity=True):
		response = self.get_client().terminate_instance_in_auto_scaling_group(
			InstanceId=instance_id,
			ShouldDecrementDesiredCapacity=reduce_capacity
		)
		return response

	def get_capacity(self, autoscaling_group):
		group = self.get_autoscaling_group(autoscaling_group)
		return group['DesiredCapacity']

	def set_capacity(self, autoscaling_group, capacity):
		self.get_client().set_desired_capacity(
			AutoScalingGroupName=autoscaling_group,
			DesiredCapacity=capacity,
			HonorCooldown=False
		)

	def get_instances(self, autoscaling_group):
		group = self.get_autoscaling_group(autoscaling_group)
		return group['Instances']

	def list_scaling_activities(self, autoscaling_group):
		response = self.get_client().describe_scaling_activities(
			AutoScalingGroupName=autoscaling_group
		)
		return response

	def list_scheduled_activities(self, autoscaling_group, start_time=datetime(2016, 1, 1),
		end_time=datetime(2100, 12, 1)):
		response = self.get_client().describe_scheduled_actions(
			AutoScalingGroupName=autoscaling_group,
			ScheduledActionNames=[],
			StartTime=start_time,
			EndTime=end_time
		)
		return response