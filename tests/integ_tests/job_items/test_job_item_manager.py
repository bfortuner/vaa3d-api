from bigneuron_app.job_items.job_item_manager import *
from bigneuron_app.clients.constants import *
import pytest

QUEUE_TIMEOUT=30 # This needs to be long enough to run vaa3d job otherwise msg will become visible again

def test_convert_dynamo_item_to_dict():
	job_item = create_job_item(1, VAA3D_TEST_INPUT_FILE_1, sqs.get_queue(SQS_JOB_ITEMS_QUEUE))
	job_item_dict = convert_dynamo_job_item_to_dict(job_item)

def test_run_job_item__complete():
	queue = sqs.create_test_queue_w_dead_letter(120, 1)
	filenames = [VAA3D_TEST_INPUT_FILE_2,VAA3D_TEST_INPUT_FILE_5,VAA3D_TEST_INPUT_FILE_7]
	for f in filenames:
		job_item = create_test_job_item(f, queue)
		run_job_item(job_item, max_runtime=60)
	
	sqs.delete_queue(queue)

def test_run_job_item__timeout():
	queue = sqs.create_test_queue_w_dead_letter(120, 1)
	filename = VAA3D_TEST_INPUT_FILE_1
	filenames = [VAA3D_TEST_INPUT_FILE_5] #VAA3D_TEST_INPUT_FILE_2 - need to mock out timeout module to test zip files
	for f in filenames:
		job_item = create_test_job_item(f, queue)
		status = run_job_item(job_item, max_runtime=1)
		assert status == 'TIMEOUT'
	sqs.delete_queue(queue)

def test_failed_job_item_retry():
	queue = sqs.create_test_queue_w_dead_letter(QUEUE_TIMEOUT, 3)
	filename = VAA3D_TEST_INPUT_FILE_4 # Corrupt file to simulate failure quickly (< MIN_RUNTIME)
	run_job_item_w_retry(filename, queue, 3, 10)
	sqs.delete_queue(queue)

def run_job_item_w_retry(filename, queue, max_retries, timeout):
	"""
	1) Create test job_item and load into queue
	2) Pull from SQS and run job item_item
	3) Fail job_item
	4) Try again before visibility timeout reached
	5) Loop until max retries reached
	"""
	queue_name = sqs.get_queue_name(queue)
	job_item = create_test_job_item(filename, queue)
	complete = False
	current_attempt = 1
	while not complete:
		print "Attempt " + str(current_attempt)
		msg = sqs.get_message_by_key(queue.url, job_item['job_item_key'])
		assert msg is not None
		process_job_item(job_item, timeout)
		msg = sqs.get_message_by_key(queue.url, job_item['job_item_key'])		
		assert msg is None
		time.sleep(max(0,QUEUE_TIMEOUT-timeout))
		current_attempt += 1
		if current_attempt > max_retries:
			msg = sqs.get_message_by_key(queue.url, job_item['job_item_key'])			
			assert msg is None
			complete = True

def create_test_job_item(filename, queue):
	# Load job item into Dynamo and SQS
	job_item_doc = build_job_item_doc(Job.query.get(1), filename) # JobItemDocument()
	store_job_item_doc(job_item_doc) # Load into Dynamo
	add_job_item_to_queue(job_item_doc.job_item_key, queue)
	s3.download_file(filename, os.path.abspath(filename), S3_INPUT_BUCKET)
	return job_item_doc.as_dict()