import sys, time
import signal
import traceback
from time import gmtime, strftime
from bigneuron_app import db
from bigneuron_app import tasks_log
from bigneuron_app.jobs.models import Job
from bigneuron_app.jobs import job_manager
from bigneuron_app.clients import sqs, dynamo
from bigneuron_app.jobs.constants import PROCESS_JOBS_CREATED_TASK, PROCESS_JOBS_IN_PROGRESS_TASK
from bigneuron_app.emails import email_manager
import bigneuron_app.clients.constants as client_constants


def poll_jobs_queue():
	count = 0
	while count < 10:
		try:
			tasks_log.info("Polling jobs created queue " + str(count))
			update_jobs_created()
			tasks_log.info("Polling jobs in-progress queue " + str(count))
			update_jobs_in_progress()
		except Exception, err:
			tasks_log.error(traceback.format_exc())
		finally:
			count += 1
			time.sleep(20)
	db.remove()

def poll_jobs_created_queue():
	while True:
		try:
			tasks_log.info("Polling jobs_created queue")
			update_jobs_created()
		except Exception, err:
			tasks_log.error("ERROR while reading and processing job_created \n" + str(err))
		finally:
			time.sleep(20)

def poll_jobs_in_progress_queue():
	while True:
		try:
			tasks_log.info("Polling jobs_in_progress queue")
			update_jobs_in_progress()
		except Exception, err:
			tasks_log.error("ERROR while reading and processing job_in_progress \n" + str(err))
		finally:
			time.sleep(20)

def update_jobs_in_progress():
	jobs_in_progress = job_manager.get_jobs_by_status("IN_PROGRESS")
	for job in jobs_in_progress:
		job_items = job_manager.get_job_items(job.job_id)
		complete = True
		has_error = False
		for job_item in job_items:
			if job_item['job_item_status'] == 'ERROR':
				has_error = True
			elif job_item['job_item_status'] in ['IN_PROGRESS', 'CREATED']:
				complete = False

		if complete:
			if has_error:
				job.status_id = job_manager.get_job_status_id("COMPLETE_WITH_ERRORS")
			else:
				job.status_id = job_manager.get_job_status_id("COMPLETE")
			db.commit()
			email_manager.send_job_complete_email(job)

def update_jobs_created():
	jobs_created = job_manager.get_jobs_by_status("CREATED")
	for job in jobs_created:
		tasks_log.info("Found new job")
		job.status_id = job_manager.get_job_status_id("IN_PROGRESS")
		db.commit()
		email_manager.send_job_created_email(job)

def signal_handler(signal, frame):
	print "Exiting..."
	sys.exit(0)



# Unit Tests #

