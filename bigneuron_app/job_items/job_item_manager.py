import sys
from bigneuron_app import db
from bigneuron_app.job_items.models import JobItem, JobItemStatus
from bigneuron_app.clients import s3, vaa3d
from bigneuron_app.clients.constants import *

def process_next_job_item():
	new_job_status = JobItemStatus.query.filter_by(status_name="CREATED").first()
	job_item = JobItem.query.filter_by(status_id=new_job_status.id).order_by(JobItem.created).first()
	if job_item is None: 
		print "No job items found in Queue"
		return
	print "Found new job_item"
	job_item.status_id = get_job_item_status_id("IN_PROGRESS")
	db.session.commit()
	process(job_item)

def process(job_item):
	try:
		print "Processing job item " + str(job_item)
		job = vaa3d.Vaa3dJob(VAA3D_TEST_JOB)
		s3.download_file(job.input_filename, job.input_file_path, S3_INPUT_BUCKET)
		vaa3d.run_job(job)
		s3.upload_file(job.output_filename, job.output_file_path, S3_OUTPUT_BUCKET)
		vaa3d.cleanup(job.input_file_path, job.output_file_path)
		job_item.status_id = get_job_item_status_id("COMPLETE")
		db.session.commit()
	except Exception as e:
		job_item.status_id = get_job_item_status_id("ERROR")
		print e
	finally:
		db.session.commit()

def get_job_items_by_status(job_status):
	job_item_status = JobItemStatus.query.filter_by(status_name=job_status).first()
	jobs = job_status.jobs.all()
	return jobs

def get_job_item_status_id(name):
	return JobItemStatus.query.filter_by(status_name=name).first().id