import time
import pytest
from bigneuron_app.clients.constants import *
from bigneuron_app.utils import id_generator
from bigneuron_app.clients.sqs import sqs


def test_get_queue_name():
	expected_queue_name = id_generator.generate_job_item_id()
	queue = get_test_queue(expected_queue_name)
	queue_name = sqs.get_queue_name(queue)
	assert queue_name == expected_queue_name

def test_clear_queue():
	# Only one clear request is allowed every 60 seconds
	queue_name = id_generator.generate_job_item_id()
	queue = get_test_queue(queue_name)
	expected_message_id = sqs.send_message(queue, 'boto3', {
    	'Author': {
        	'StringValue': 'Daniel',
        	'DataType': 'String'
    	}
	})
	msgs = sqs.get_messages(queue.url)
	assert len(msgs) == 1
	sqs.clear_queue(queue)
	sqs.delete_queue(queue)

@pytest.mark.skipif(True, reason="Too slow")
def test_delete_queue():
	"""
	SLOW! Takes 60 seconds to delete a queue
	"""
	queue_name = id_generator.generate_job_item_id()
	queue = get_test_queue(queue_name)
	resp = sqs.delete_queue(queue)
	time.sleep(90)
	queue = sqs.get_queue(queue_name)
	assert queue is None

def test_get_queue():
	fake_queue = sqs.get_queue("fake-queue")
	assert fake_queue is None

	queue_name = id_generator.generate_job_item_id()
	queue = sqs.create_queue(queue_name)
	assert queue is not None

def test_get_queue_attributes():
	queue_name = id_generator.generate_job_item_id()
	queue = get_test_queue(queue_name)
	expected_message_id = sqs.send_message(queue, 'boto3', {
    	'Author': {
        	'StringValue': 'Daniel',
        	'DataType': 'String'
    	}
	})
	attributes = sqs.get_queue_attributes(queue.url)
	assert attributes is not None
	sqs.clear_queue(queue)
	sqs.delete_queue(queue)

def test_get_queue_size():
	queue_name = id_generator.generate_job_item_id()
	queue = get_test_queue(queue_name)
	expected_message_id = sqs.send_message(queue, 'boto3', {
    	'Author': {
        	'StringValue': 'Daniel',
        	'DataType': 'String'
    	}
	})
	size = sqs.get_queue_size(queue.url)
	assert size == 1
	sqs.clear_queue(queue)
	sqs.delete_queue(queue)

def test_get_all_queues():
	queues = sqs.get_all_queues()
	assert len(queues) > 0	

def test_get_message_attributes():
	queue_name = id_generator.generate_job_item_id()
	queue = get_test_queue(queue_name)
	expected_message_id = sqs.send_message(queue, 'boto3', {
    	'Author': {
        	'StringValue': 'Daniel',
        	'DataType': 'String'
    	}
	})
	message = sqs.get_next_message(queue)
	assert message['Attributes'] is not None
	print message['Attributes']['ApproximateReceiveCount']
	print message['Attributes']['ApproximateFirstReceiveTimestamp']

def test_create_queue():
	queue_name = id_generator.generate_job_item_id()
	dead_letter_queue_name = queue_name + "_dead"

	dead_queue = sqs.create_queue(dead_letter_queue_name, 43200)
	
	dead_arn = dead_queue.attributes['QueueArn']
	redrive_policy = {"maxReceiveCount":5, "deadLetterTargetArn":dead_arn}
	new_queue = sqs.create_queue(queue_name, 30, redrive_policy)

	sqs.delete_queue(dead_queue)
	sqs.delete_queue(new_queue)

def test_retry_logic():
	VISIBILITY_TIMEOUT = 2
	MAX_RECEIVE_COUNT = 2
	queue_name = id_generator.generate_job_item_id()
	dead_letter_queue_name = queue_name + "_dead"

	dead_queue = sqs.create_queue(dead_letter_queue_name, 43200)
	
	dead_arn = dead_queue.attributes['QueueArn']
	redrive_policy = {"maxReceiveCount":MAX_RECEIVE_COUNT, "deadLetterTargetArn":dead_arn}
	queue = sqs.create_queue(queue_name, VISIBILITY_TIMEOUT, redrive_policy)

	# Create Message
	expected_message_id = sqs.send_message(queue, 'boto3', {
    	'Author': {
        	'StringValue': 'Daniel',
        	'DataType': 'String'
    	}
	})

	# 1st message request succeeds
	message = sqs.get_next_message(queue)
	assert message['MessageId'] == expected_message_id

	# Visibilty Timeout not exceeded
	message = sqs.get_next_message(queue)
	assert message is None

	# Visibilty Timeout exceeded
	time.sleep(VISIBILITY_TIMEOUT)

	# 2nd message request succeeds
	message = sqs.get_next_message(queue)
	assert message['MessageId'] == expected_message_id

	# Visibilty Timeout exceeded
	time.sleep(VISIBILITY_TIMEOUT)

	# 3rd message request fails - MAX_RECEIVE_COUNT exceeded
	message = sqs.get_next_message(queue)
	assert message is None

	# 3rd message in Dead Letter Queue
	message = sqs.get_next_message(dead_queue)
	assert message['MessageId'] == expected_message_id

	# Cleanup
	time.sleep(VISIBILITY_TIMEOUT)
	sqs.delete_queue(dead_queue)
	sqs.delete_queue(queue)

def test_send_and_get_message():
	queue_name = id_generator.generate_job_item_id()
	queue = get_test_queue(queue_name)
	message_id = sqs.send_message(queue, 'boto3', {
    	'Author': {
        	'StringValue': 'Daniel',
        	'DataType': 'String'
    	}
	})
	time.sleep(5)  # Accounts for 5 second delivery delay
	message = sqs.get_next_message(queue)
	assert message_id == message['MessageId']
	sqs.delete_queue(queue)

def test_get_message_by_key():
	TEST_JOB_ITEM_KEY = id_generator.generate_job_item_id()
	queue_name = id_generator.generate_job_item_id()
	queue = get_test_queue(queue_name)
	message_id = sqs.send_message(queue, 'boto3', {
		"job_item_key" : { 
			"StringValue" : TEST_JOB_ITEM_KEY, 
			"DataType" : "String"
		},
		"job_type" : { 
			"StringValue" : "process_job_item", 
			"DataType" : "String"
		}
	})
	message = sqs.get_message_by_key(queue.url, TEST_JOB_ITEM_KEY)
	assert message_id == message['MessageId']
	assert message['MessageAttributes']['job_item_key']['StringValue'] == TEST_JOB_ITEM_KEY
	sqs.delete_queue(queue)

def test_update_msg_visibility_timeout():
	job_item_key = id_generator.generate_job_item_id()
	queue_name = id_generator.generate_job_item_id()
	queue = get_test_queue(queue_name)

	attribs = {}
	attribs['VisibilityTimeout'] = str(120)
	sqs.set_queue_attributes(queue, attribs)

	message_id = sqs.send_message(queue, 'boto3', {
		"job_item_key" : { 
			"StringValue" : job_item_key, 
			"DataType" : "String"
		}
	})
	# 1st Try
	message = sqs.get_message_by_key(queue.url, job_item_key)
	msg_receipt = message['ReceiptHandle']
	assert message is not None

	# 2nd - Visibilty Timeout not exceeded
	message = sqs.get_message_by_key(queue.url, job_item_key)
	assert message is None

	new_timeout = 10
	response = sqs.update_msg_visibility_timeout(queue.url, 
		msg_receipt, new_timeout)

	# 3rd - Visibilty Timeout not exceeded
	message = sqs.get_message_by_key(queue.url, job_item_key)
	assert message is None

	# Visibilty Timeout exceeded
	time.sleep(new_timeout)

	# 4th message request succeeds
	message = sqs.get_next_message(queue)
	assert message['MessageId'] == message_id

	sqs.delete_queue(queue)

def get_test_queue(queue_name):
	queue = sqs.create_queue(queue_name)
	return queue

## Message request structure
msg_text="{{job_item_id}}"
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
