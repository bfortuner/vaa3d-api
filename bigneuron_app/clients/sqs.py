import boto3
import time

from bigneuron_app.clients.constants import AWS_REGION, AWS_ACCESS_KEY, AWS_SECRET_KEY
from bigneuron_app.clients.constants import SQS_JOB_ITEMS_QUEUE, SQS_JOBS_QUEUE


def get_connection():
	return boto3.resource('sqs', region_name=AWS_REGION, 
		aws_access_key_id=AWS_ACCESS_KEY, 
		aws_secret_access_key=AWS_SECRET_KEY)

def get_client():
	return boto3.client('sqs', region_name=AWS_REGION, 
		aws_access_key_id=AWS_ACCESS_KEY, 
		aws_secret_access_key=AWS_SECRET_KEY)

def get_queue(conn, queue_name):
	if queue_exists(conn, queue_name):
		return conn.get_queue_by_name(QueueName=queue_name)
	return None

def get_queue_name(queue):
	start_pos = queue.url.rfind('/')
	name = queue.url[start_pos+1:]
	return name

def get_all_queues(conn):
	queues = []
	for queue in conn.queues.all():
		queues.append(queue)
	return queues

def queue_exists(conn, queue_name):
	queues = get_all_queues(conn)
	for queue in queues:
		if get_queue_name(queue) == queue_name:
			return True
	return False

def create_queue(conn, queue_name):
	return conn.create_queue(
		QueueName=queue_name, 
		Attributes={'DelaySeconds': '5'})

def delete_queue(queue_name):
	""" 
	Takes up to 60 seconds 
	"""
	conn = get_connection()
	client = get_client()
	queue = get_queue(conn, queue_name)
	if queue:
		print "Deleting queue"
		client.delete_queue(QueueUrl=queue.url)
		time.sleep(60)
	print "Queue does not exist"

def clear_queue(queue_name):
	conn = get_connection()
	client = get_client()
	queue = get_queue(conn, queue_name)
	messages = get_messages(client, queue.url, num_msgs=10)
	if len(messages) == 0:
		return
	while len(messages) > 0:
		for message in messages:
			delete_message(client, queue, message)
		messages = get_messages(client, queue.url, num_msgs=10)

def send_message(queue, msg_text, msg_dict={}):
	"""
	queue: sqs queue object
	msg_text: required text
	msg_dict: optional dictionary of key-value pairs
	"""
	response = queue.send_message(MessageBody=msg_text, MessageAttributes=msg_dict)
	message_id = response.get('MessageId')
	md5 = response.get('MD5OfMessageBody')
	return message_id

def get_messages(client, queue_url, num_msgs=1):
	response = client.receive_message(
		QueueUrl=queue_url,
		MaxNumberOfMessages=num_msgs,
		MessageAttributeNames=['All'])
	print "Response is " + str(response)
	if 'Messages' in response:
		return response['Messages']
	return []

def get_next_message(client, queue):
	messages = get_messages(client, queue.url, 1)
	print messages
	if len(messages) < 1:
		return None
	return messages[0]

def delete_message(client, queue, msg):
	response = client.delete_message(
    	QueueUrl=queue.url,
    	ReceiptHandle=msg['ReceiptHandle']
	)
	return response

def drop_and_recreate_queue(queue_name):
	conn = get_connection()
	if queue_exists(conn, queue_name):
		print "Clearing existing SQS queue " + queue_name
		clear_queue(queue_name)
	else:
		print "Creating new SQS queue " + queue_name
		new_queue = create_queue(conn, queue_name)	






### Unit Tests ###

def test_get_queue_name():
	queue_name = "test"
	conn = get_connection()
	queue = get_queue(conn, queue_name)
	exp_queue_name = get_queue_name(queue)
	print exp_queue_name
	assert(queue_name == exp_queue_name)

def test_clear_queue():
	queue_name = "test"
	conn = get_connection()
	client = get_client()
	queue = get_queue(conn, queue_name)
	clear_queue(queue_name)
	msgs = get_messages(client, queue.url)
	assert len(msgs) == 0

def test_get_queue():
	conn = get_connection()
	fake_queue = get_queue(conn, "fake-queue")
	print fake_queue

def test_all():
	conn = get_connection()
	client = get_client()
	#new_queue = create_queue(conn, "test")
	new_queue = get_queue(conn, "test")
	print new_queue.url

	queues = get_all_queues(conn)
	print queues

	message_id = send_message(new_queue, 'boto3', {
    	'Author': {
        	'StringValue': 'Daniel',
        	'DataType': 'String'
    	}
	})
	print message_id

	message_id = send_message(new_queue, 'boto3', {
		"job_item_key" : { 
			"StringValue" : "OINOINON", 
			"DataType" : "String"
		},
		"job_type" : { 
			"StringValue" : "process_job_item", 
			"DataType" : "String"
		}
	})

	message = get_next_message(client, new_queue)
	print message

	message = get_next_message(client, new_queue)
	print message
	#print message["MessageId"] == message_id

	clear_queue(new_queue.name)
	#delete_queue(new_queue.name)





## Message request structure

msg_text="job_item: {{job_item_id}}"
msg_dict= { "message_type": "job_item",
			"job_item_id" : "job-item-id"}


## Messages Response Syntax

"""
{
    'Messages': [
        {
            'MessageId': 'string',
            'ReceiptHandle': 'string',
            'MD5OfBody': 'string',
            'Body': 'string',
            'Attributes': {
                'string': 'string'
            },
            'MD5OfMessageAttributes': 'string',
            'MessageAttributes': {
                'string': {
                    'StringValue': 'string',
                    'BinaryValue': b'bytes',
                    'StringListValues': [
                        'string',
                    ],
                    'BinaryListValues': [
                        b'bytes',
                    ],
                    'DataType': 'string'
                }
            }
        },
    ]
}

"""
