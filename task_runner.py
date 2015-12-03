import sys
import signal
from multiprocessing import Process

import bigneuron_app.job_items.tasks as job_item_tasks
import bigneuron_app.jobs.tasks as job_tasks


def start_workers():
	"""
	Use this for manually managing processes
	"""
	print "Starting workers.."
	jobs_worker = Process(name='jobs_worker', target=job_tasks.poll_jobs_queue)
	#jobs_in_progress_worker = Process(name='jobs_in_progress_worker', target=job_tasks.poll_jobs_in_progress_queue)
	job_items_worker = Process(name='job_items_worker', target=job_item_tasks.poll_job_items_queue)

	print "starting worker " + jobs_worker.name
	jobs_worker.start()
	#print "starting worker " + jobs_in_progress_worker.name
	#jobs_in_progress_worker.start()
	print "starting worker " + job_items_worker.name
	job_items_worker.start()

def start_process(method_name):
	"""
	Using this with Circus workers
	"""
	if method_name == "jobs":
		job_tasks.poll_jobs_queue()
	elif method_name == "job_items":
		job_item_tasks.poll_job_items_queue()

def signal_handler(signal, frame):
	print "Exiting..."
	sys.exit(0)


if __name__ == "__main__":
	method = sys.argv[1]
	start_process(method)
	#signal.signal(signal.SIGINT, signal_handler)
	#start_workers()
