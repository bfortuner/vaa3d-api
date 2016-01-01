import time
from bigneuron_app import db
from bigneuron_app import jobs_log
from bigneuron_app.emails import email_manager
from bigneuron_app.jobs.models import Job, JobStatus
from bigneuron_app.job_items.models import JobItemStatus
from bigneuron_app.users.models import User
from bigneuron_app.job_items import job_item_manager
from bigneuron_app.clients import s3, dynamo
from bigneuron_app.clients.sqs import SQS
from bigneuron_app.clients.constants import *
from bigneuron_app.jobs.constants import OUTPUT_FILE_SUFFIXES
from bigneuron_app.emails.constants import ADMIN_EMAIL
from bigneuron_app.utils import zipper
from bigneuron_app.utils.constants import USER_JOB_LOG_EXT

sqs = SQS()

def get_job(job_id):
	job = Job.query.get(job_id)
	job_dict = job.as_dict()
	job_dict['job_status'] = job.job_status.status_name
	link_expiry_secs = 3600 # 1 hour
	s3_conn = s3.S3Connection(VAA3D_USER_AWS_ACCESS_KEY, VAA3D_USER_AWS_SECRET_KEY)
	job_dict['download_url'] = s3.get_download_url(s3_conn, S3_OUTPUT_BUCKET, 
		job.get_output_s3_key(), link_expiry_secs)
	return job_dict	

def get_job_items(job_id, include_zip=True):
	dynamo_conn = dynamo.get_connection()
	table = dynamo.get_table(dynamo_conn, DYNAMO_JOB_ITEMS_TABLE)
	job_items = dynamo.query_all(table, "job_index", "job_id", job_id)
	link_expiry_secs = 3600 # 1 hour
	s3_conn = s3.S3Connection(VAA3D_USER_AWS_ACCESS_KEY, VAA3D_USER_AWS_SECRET_KEY)
	job_items_list = []
	for item in job_items:
		if include_zip or not zipper.is_compressed_filename(item['input_filename']):
			item_dict = job_item_manager.convert_dynamo_job_item_to_dict(item)
			item_dict['job_item_status'] = JobItemStatus.query.get(int(item_dict['status_id'])).status_name
			output_s3_key = item_dict['output_dir'] + "/" + item_dict['output_filename']
			item_dict['download_url'] = s3.get_download_url(s3_conn, S3_OUTPUT_BUCKET, 
				output_s3_key, link_expiry_secs)
			logs_s3_key = item_dict['output_dir'] + "/logs/" + item_dict['output_filename'] + USER_JOB_LOG_EXT
			item_dict['logs_download_url'] = s3.get_download_url(s3_conn, S3_OUTPUT_BUCKET, 
				logs_s3_key, link_expiry_secs)
			job_items_list.append(item_dict)
	return job_items_list

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
	db.add(job)
	db.commit()

	job_item_queue = sqs.get_queue(SQS_JOB_ITEMS_QUEUE)
	for f in data['filenames']:
		job_item_doc = job_item_manager.build_job_item_doc(job, f)
		job_item_manager.store_job_item_doc(job_item_doc)
		job_item_manager.add_job_item_to_queue(job_item_doc.job_item_key, 
			job_item_queue)

	return job.job_id

def get_jobs_by_status(job_status):
	job_status = JobStatus.query.filter_by(status_name=job_status).first()
	jobs = job_status.jobs.all()
	return jobs

def get_job_status_id(name):
	return JobStatus.query.filter_by(status_name=name).first().id

def get_output_file_suffix(plugin_name, settings):
	return OUTPUT_FILE_SUFFIXES[plugin_name]

	