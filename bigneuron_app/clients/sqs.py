import boto3
import json
import time
from bigneuron_app.clients.constants import *
from bigneuron_app import items_log
from bigneuron_app.utils import id_generator


class SQS:
	def __init__(self):
		self.conn = None
		self.client = None

	def get_conn(self):
		if self.conn:
			return self.conn
		self.conn = boto3.resource('sqs', region_name=AWS_REGION, 
			aws_access_key_id=AWS_ACCESS_KEY, 
			aws_secret_access_key=AWS_SECRET_KEY)
		return self.conn

	def get_client(self):
		if self.client:
			return self.client
		return boto3.client('sqs', region_name=AWS_REGION, 
			aws_access_key_id=AWS_ACCESS_KEY, 
			aws_secret_access_key=AWS_SECRET_KEY)

	def get_queue(self, queue_name):
		if self.queue_exists(queue_name):
			return self.get_conn().get_queue_by_name(QueueName=queue_name)
		return None

	def get_queue_name(self, queue):
		start_pos = queue.url.rfind('/')
		name = queue.url[start_pos+1:]
		return name

	def get_all_queues(self):
		queues = []
		for queue in self.get_conn().queues.all():
			queues.append(queue)
		return queues

	def queue_exists(self, queue_name):
		queues = self.get_all_queues()
		for queue in queues:
			if self.get_queue_name(queue) == queue_name:
				return True
		return False

	def create_queue(self, queue_name, timeout=30, redrive_policy=None):
		attributes = {
			'DelaySeconds': '0',
			'VisibilityTimeout' : str(timeout),
		}
		if redrive_policy:
			attributes['RedrivePolicy'] = json.dumps(redrive_policy)
		return self.get_conn().create_queue(
			QueueName=queue_name, 
			Attributes=attributes
		)

	def delete_queue(self, queue):
		""" 
		Takes up to 60 seconds 
		"""
		return self.get_client().delete_queue(QueueUrl=queue.url)

	def clear_queue(self, queue):
		""" 
		Only one purge request is allowed every 60 seconds
		"""
		self.get_client().purge_queue(QueueUrl=queue.url)

	def send_message(self, queue, msg_text, msg_dict={}):
		"""
		queue: sqs queue object
		msg_text: required text
		msg_dict: optional dictionary of key-value pairs
		"""
		response = queue.send_message(MessageBody=msg_text, MessageAttributes=msg_dict)
		message_id = response.get('MessageId')
		md5 = response.get('MD5OfMessageBody')
		return message_id

	def get_messages(self, queue_url, num_msgs=1):
		response = self.get_client().receive_message(
			QueueUrl=queue_url,
			MaxNumberOfMessages=num_msgs,
			AttributeNames=['All'],
			MessageAttributeNames=['All'])
		if 'Messages' in response:
			return response['Messages']
		return []

	def get_next_message(self, queue):
		messages = self.get_messages(queue.url, 1)
		if len(messages) < 1:
			return None
		message = messages[0]
		return message

	def delete_message(self, queue, msg):
		response = self.get_client().delete_message(
	    	QueueUrl=queue.url,
	    	ReceiptHandle=msg['ReceiptHandle']
		)
		return response

	def drop_and_recreate_queue(self, queue_name, dead_queue_name, timeout, max_receive):
		dead_queue = self.get_queue(dead_queue_name)
		if dead_queue:
			print "Dropping existing SQS dead queue " + dead_queue_name
			#self.clear_queue(queue)
			self.delete_queue(dead_queue)
			time.sleep(62)

		queue = self.get_queue(queue_name)
		if queue:
			print "Dropping existing SQS queue " + queue_name
			#self.clear_queue(queue)
			self.delete_queue(queue)
			time.sleep(62)
		print "Creating new SQS queue " + queue_name
		return self.create_queue_w_dead_letter(queue_name, dead_queue_name, 
			timeout, max_receive)

	def get_message_by_key(self, queue_url, key):
		"""
		Used for testing. Not how SQS is designed to be used.
		"""
		msgs = self.get_messages(queue_url, 10)
		for msg in msgs:
			job_item_key = msg['MessageAttributes']['job_item_key']['StringValue']
			if job_item_key == key:
				return msg
		return None

	def update_msg_visibility_timeout(self, queue_url, receipt, timeout):
		response = self.get_client().change_message_visibility(
			QueueUrl=queue_url,
			ReceiptHandle=receipt,
			VisibilityTimeout=timeout #seconds
		)
		return response

	def get_queue_attributes(self, queue_url):
		response = self.get_client().get_queue_attributes(
			QueueUrl=queue_url,
			AttributeNames=['All']
		)
		return response['Attributes']

	def set_queue_attributes(self, queue, attribs_dict):
		response = queue.set_attributes(
    		Attributes=attribs_dict
		)
		return response

	def get_queue_size(self, queue_url):
		attributes = self.get_queue_attributes(queue_url)
		visible = int(attributes['ApproximateNumberOfMessages'])
		not_visible = int(attributes['ApproximateNumberOfMessagesNotVisible'])
		return visible + not_visible

	def create_queue_w_dead_letter(self, queue_name, dead_queue_name, timeout, max_receive):
		dead_queue = self.create_queue(dead_queue_name, 35000)
		
		dead_arn = dead_queue.attributes['QueueArn']
		redrive_policy = {"maxReceiveCount":max_receive, "deadLetterTargetArn":dead_arn}
		new_queue = self.create_queue(queue_name, timeout, redrive_policy)
		return new_queue

	def create_test_queue_w_dead_letter(self, timeout, max_receive):
		queue_name = id_generator.generate_job_item_id()
		dead_queue_name = queue_name + "_dead"
		return self.create_queue_w_dead_letter(queue_name, dead_queue_name, 
			timeout, max_receive)

sqs = SQS()
