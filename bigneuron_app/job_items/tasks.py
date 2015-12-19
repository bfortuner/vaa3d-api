import sys, time
import traceback
from time import gmtime, strftime
import signal
from bigneuron_app import db
from bigneuron_app import tasks_log, items_log
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
	sqs = SQS()
	tasks_log.info("Getting next job_item from queue")
	queue = sqs.get_queue(client_constants.SQS_JOB_ITEMS_QUEUE)
	msg = sqs.get_next_message(queue)
	if msg is None: 
		tasks_log.info("No job items found in Queue")
		return
	job_item_key = msg['MessageAttributes']['job_item_key']['StringValue']
	tasks_log.info("Found new job_item " + job_item_key)
	job_item = job_item_manager.get_job_item_doc(job_item_key)
	job_item['attempts'] += 1
	status = job_item_manager.process_job_item(job_item)
	if status == "COMPLETE":
		items_log.info("Deleting completed job_item from queue")
		sqs.delete_message(queue, msg)
	else:
		# We are going to let SQS handle retries
		items_log.info("Leaving job_item in queue")


# Unit Tests #

def test_process_next_job_item():
	sqs = SQS()
	queue = sqs.get_queue(client_constants.SQS_JOB_ITEMS_QUEUE)
	job = Job(1, 1, "mytestdir", client_constants.VAA3D_DEFAULT_PLUGIN, 
		client_constants.VAA3D_DEFAULT_FUNC, 1, client_constants.VAA3D_DEFAULT_OUTPUT_SUFFIX)
	db.add(job)
	db.commit()
	job_item = job_item_manager.create_job_item(job.job_id, client_constants.VAA3D_TEST_INPUT_FILE_1, queue)
	print "JOB_ITEM_KEY " + job_item['job_item_key']
	process_next_job_item()
