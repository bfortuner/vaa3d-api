import sys, time
import traceback
from time import gmtime, strftime
import signal
from bigneuron_app import db
from bigneuron_app import tasks_log
from bigneuron_app.job_items.models import JobItemStatus, JobItemDocument
from bigneuron_app.jobs.models import Job
from bigneuron_app.job_items import job_item_manager
from bigneuron_app.clients.sqs import SQS
from bigneuron_app.job_items.constants import PROCESS_JOB_ITEM_TASK
import bigneuron_app.clients.constants as client_constants
from bigneuron_app.utils import logger

POLL_JOB_ITEMS_SLEEP=2
POLL_JOB_ITEMS_MAX_RUNS=10

def poll_job_items_queue():
	count = 0
	while count < POLL_JOB_ITEMS_MAX_RUNS:
		try:
			tasks_log.info("Polling job_items queue " + str(count))
			process_next_job_item()
		except Exception, err:
			tasks_log.error(traceback.format_exc())
		finally:
			count+=1
			time.sleep(POLL_JOB_ITEMS_SLEEP)
	db.remove()

def process_next_job_item():
	job_item_key = get_next_job_item_from_queue()
	if job_item_key is None: 
		tasks_log.info("No job items found in Queue")
		return
	tasks_log.info("Found new job_item")
	job_item = job_item_manager.get_job_item_doc(job_item_key)
	job_item['attempts'] += 1
	job_item_manager.process_job_item(job_item)

def get_next_job_item_from_queue():
	sqs = SQS()
	tasks_log.info("Getting next job_item from queue")
	queue = sqs.get_queue(client_constants.SQS_JOB_ITEMS_QUEUE)
	msg = sqs.get_next_message(queue)
	if msg is None:
		return None
	job_item_key = msg['MessageAttributes']['job_item_key']['StringValue']
	#We're going to rely on SQS and it's retry policy to handle this
	#This way if a server/process crashes unexpectedly we will retry it a few times before deleting
	#sqs.delete_message(client, queue, msg)
	return job_item_key

def signal_handler(signal, frame):
	print "Exiting..."
	sys.exit(0)



# Unit Tests #

def test_process_next_job_item():
	job = Job(1, 1, "mytestdir", client_constants.VAA3D_DEFAULT_PLUGIN, 
		client_constants.VAA3D_DEFAULT_FUNC, 1, client_constants.VAA3D_DEFAULT_OUTPUT_SUFFIX)
	db.add(job)
	db.commit()
	job_item = job_item_manager.create_job_item(job.job_id, client_constants.VAA3D_TEST_INPUT_FILE_1)
	print "JOB_ITEM_KEY " + job_item['job_item_key']
	process_next_job_item()

def test_get_next_job_item_from_queue():
	job_item_key = get_next_job_item_from_queue()
	print job_item_key

