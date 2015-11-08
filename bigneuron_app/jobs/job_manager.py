from bigneuron_app import db
from bigneuron_app.emails import email_manager
from bigneuron_app.jobs.models import Job, JobStatus
from bigneuron_app.job_items.models import JobItem
from bigneuron_app.job_items import job_item_manager
from bigneuron_app.clients import s3
from bigneuron_app.clients.constants import S3_INPUT_BUCKET

def get_user_input_filenames(user_id):
	return s3.get_all_files(S3_INPUT_BUCKET)

def create_job(filenames, user):
	job = Job(user.id, 1) #Status = CREATED
	db.session.add(job)
	db.session.commit()

	for f in filenames:
		job_item = JobItem(job.job_id, f, 1) #Status = CREATED
		db.session.add(job_item)
	db.session.commit()

	return job.job_id

def update_jobs_in_progress():
	jobs_in_progress = get_jobs_by_status("IN_PROGRESS")
	for job in jobs_in_progress:
		job_items = job.job_items.all()
		complete = True
		has_error = False
		for job_item in job_items:
			if job_item.status_id == job_item_manager.get_job_item_status_id("ERROR"):
				has_error = True
			elif job_item.status_id in [job_item_manager.get_job_item_status_id("IN_PROGRESS"), 
					job_item_manager.get_job_item_status_id("CREATED")]:
				complete = False

		if complete:
			if has_error:
				job.status_id = get_job_status_id("COMPLETE_WITH_ERRORS")
			else:
				job.status_id = get_job_status_id("COMPLETE")
			db.session.commit()
			email_manager.send_job_complete_email(job)

def update_jobs_created():
	jobs_created = get_jobs_by_status("CREATED")
	for job in jobs_created:
		job.status_id = get_job_status_id("IN_PROGRESS")
	db.session.commit()

def get_jobs_by_status(job_status):
	job_status = JobStatus.query.filter_by(status_name=job_status).first()
	jobs = job_status.jobs.all()
	return jobs

def get_job_status_id(name):
	return JobStatus.query.filter_by(status_name=name).first().id