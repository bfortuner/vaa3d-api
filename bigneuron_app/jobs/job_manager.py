import time
from bigneuron_app import db
from bigneuron_app.emails import email_manager
from bigneuron_app.jobs.models import Job, JobStatus
from bigneuron_app.job_items.models import JobItem
from bigneuron_app.users.models import User
from bigneuron_app.job_items import job_item_manager
from bigneuron_app.clients import s3
from bigneuron_app.clients.constants import S3_INPUT_BUCKET, S3_OUTPUT_BUCKET
from bigneuron_app.clients.constants import VAA3D_USER_AWS_ACCESS_KEY, VAA3D_USER_AWS_SECRET_KEY
from bigneuron_app.jobs.constants import OUTPUT_FILE_SUFFIXES
from bigneuron_app.emails.constants import ADMIN_EMAIL

def get_job(job_id):
	job = Job.query.get(job_id)
	job_dict = job.as_dict()
	job_dict['job_status'] = job.job_status.status_name
	link_expiry_secs = 3600 # 1 hour
	s3_conn = s3.S3Connection(VAA3D_USER_AWS_ACCESS_KEY, VAA3D_USER_AWS_SECRET_KEY)
	job_dict['download_url'] = s3.get_download_url(s3_conn, S3_OUTPUT_BUCKET, 
		job.get_output_s3_key(), link_expiry_secs)
	return job_dict	

def get_job_items(job_id):
	job_items = JobItem.query.filter_by(job_id=job_id)
	link_expiry_secs = 3600 # 1 hour
	s3_conn = s3.S3Connection(VAA3D_USER_AWS_ACCESS_KEY, VAA3D_USER_AWS_SECRET_KEY)
	job_items_dict_list = []
	for item in job_items:
		item_dict = item.as_dict()
		item_dict['job_item_status'] = item.job_item_status.status_name
		item_dict['output_filename'] = item.get_output_filename()
		item_dict['download_url'] = s3.get_download_url(s3_conn, S3_OUTPUT_BUCKET, 
			item.get_output_s3_key(), link_expiry_secs)
		job_items_dict_list.append(item_dict)
	return job_items_dict_list

def get_user_input_filenames(user_id):
	return s3.get_all_files(S3_INPUT_BUCKET)

def create_job(user, data):
	plugin_name = data['plugin']['name']
	method = data['plugin']['method']
	settings = data['plugin']['settings']
	output_file_suffix = get_output_file_suffix(plugin_name, settings)
	channel = data['plugin']['settings']['params']['channel']
	job = Job(user.id, 1, data['outputDir'], plugin_name, method, 
		channel, output_file_suffix)
	db.session.add(job)
	db.session.commit()

	for f in data['filenames']:
		job_item_doc = job_item_manager.build_job_item_doc(job, f)
		job_item_manager.create_job_item_doc(job_item_doc)
		job_item = JobItem(job.job_id, f, 1)
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
		email_manager.send_job_created_email(job)

def get_jobs_by_status(job_status):
	job_status = JobStatus.query.filter_by(status_name=job_status).first()
	jobs = job_status.jobs.all()
	return jobs

def get_job_status_id(name):
	return JobStatus.query.filter_by(status_name=name).first().id

def get_output_file_suffix(plugin_name, settings):
	return OUTPUT_FILE_SUFFIXES[plugin_name]




## Unit Tests ##

def test_all():
	data = {
		"output_dir" : "testdir",
		"plugin" : {
			"name" : "test_plugin",
			"method" : "test_method",
			"settings" : {
				"params" : {
					"channel" : 1
				}
			}
		},

	}
	user = user_manager.get_or_create_user(ADMIN_EMAIL)
	job = create_job(user, data)

	# plugin_name = data['plugin']['name']
	# method = data['plugin']['method']
	# settings = data['plugin']['settings']
	# output_dir = data['outputDir']
	# channel = data['plugin']['settings']['params']['channel']
	# output_file_suffix = get_output_file_suffix(plugin_name, settings)
	# job = Job(user.id, 1, output_dir, plugin_name, method, 
	# 	channel, output_file_suffix)

	