import sys
import traceback
import zipfile
import shutil
import time
from bigneuron_app import db
from bigneuron_app import items_log
from bigneuron_app.job_items.models import JobItemStatus, JobItemDocument
from bigneuron_app.jobs.models import Job
from bigneuron_app.clients import s3, vaa3d, dynamo
from bigneuron_app.clients.sqs import SQS
from bigneuron_app.clients.constants import *
from bigneuron_app.job_items.constants import PROCESS_JOB_ITEM_TASK
from bigneuron_app.jobs.constants import OUTPUT_FILE_SUFFIXES, PLUGINS
from bigneuron_app.utils import zipper
from bigneuron_app.utils.constants import USER_JOB_LOG_EXT
from decimal import Decimal
from bigneuron_app.utils.exceptions import MaxRuntimeException


sqs = SQS()

def process_job_item(job_item, timeout=None):
	job_item['status_id'] = get_job_item_status_id("IN_PROGRESS")
	save_job_item(job_item)
	local_file_path = os.path.abspath(job_item['input_filename'])
	bucket_name = s3.get_bucket_name_from_filename(job_item['input_filename'], 
		[S3_INPUT_BUCKET, S3_WORKING_INPUT_BUCKET])
	s3.download_file(job_item['input_filename'], local_file_path, bucket_name)
	if not timeout:
		timeout = vaa3d.get_timeout(local_file_path)
	status = run_job_item(job_item, timeout)
	return status

def run_job_item(job_item, timeout):
	items_log.info("running job item " + str(job_item))
	local_file_path = os.path.abspath(job_item['input_filename'])
	job_item_status = "ERROR"
	try:
		if zipper.is_zip_file(local_file_path):
			process_zip_file(job_item, local_file_path, timeout)
		else:
			process_non_zip_file(job_item, timeout)
		job_item_status = "COMPLETE"
	except MaxRuntimeException as e:	
		items_log.error(str(e) + traceback.format_exc())		
	except Exception as e:
		items_log.error(traceback.format_exc())
	finally:
		print "Status " + job_item_status
		job_item['status_id'] = get_job_item_status_id(job_item_status)
		#job_item['status_id'] = get_status_id_with_retry(job_item)
		save_job_item(job_item)
		return job_item_status

def get_status_id_with_retry(job_item):
	status_id = job_item['status_id']
	attempts = job_item['attempts']
	if status_id == get_job_item_status_id("ERROR") and attempts < SQS_MAX_RECEIVES:
		return get_job_item_status_id("CREATED")
	return status_id

def get_job_items_by_status(job_status):
	job_item_status = JobItemStatus.query.filter_by(status_name=job_status).first()
	jobs = job_status.jobs.all()
	return jobs

def get_job_item_status_id(name):
	return JobItemStatus.query.filter_by(status_name=name).first().id

def upload_output_file(output_dir, output_filename):
	output_file_path = os.path.abspath(output_filename)
	s3_key = output_dir + "/" + output_filename
	s3.upload_file(s3_key, output_file_path, S3_OUTPUT_BUCKET)
	return output_file_path

def upload_log_file(output_dir, output_filename):
	log_file_path = os.path.abspath(output_filename + USER_JOB_LOG_EXT)
	s3_key = output_dir + "/logs/" + output_filename + USER_JOB_LOG_EXT
	s3.upload_file(s3_key, log_file_path, S3_OUTPUT_BUCKET)
	return log_file_path

def process_non_zip_file(job_item, timeout):
	# This will still throw an exception despite finally
	input_file_path = os.path.abspath(job_item['input_filename'])
	log_file_path = None
	output_file_path = None
	try:
		vaa3d.run_job(job_item, timeout)
		output_file_path = upload_output_file(job_item['output_dir'], job_item['output_filename'])
	finally:
		log_file_path = upload_log_file(job_item['output_dir'], job_item['output_filename'])
		vaa3d.cleanup_all([input_file_path, log_file_path]) #swc files already included

def process_zip_file(job_item, zip_file_path, timeout):
	"""
	Unzip compressed file
	Create new job_item record(s)
	Upload new uncompressed file(s) to s3
	"""
	output_dir = os.path.dirname(zip_file_path)
	zip_archive = zipfile.ZipFile(zip_file_path, "r")
	filenames = zip_archive.namelist()
	if len(filenames) > 1:
		items_log.info("found more than 1 file inside .zip")
		output_dir = os.path.join(output_dir, zip_file_path[:zip_file_path.find(zipper.ZIP_FILE_EXT)])
		zipper.expand_zip_archive(zip_archive, output_dir)
		zip_archive.close()
		create_job_items_from_directory(job_item, output_dir)
		shutil.rmtree(output_dir)
	else:
		items_log.info("found only 1 file inside .zip")
		filename = filenames[0]
		file_path = os.path.join(output_dir, filename)
		zipper.extract_file_from_archive(zip_archive, filename, file_path)
		zip_archive.close()
		job_item['input_filename'] = filename
		timeout = vaa3d.get_timeout(file_path)
		print "FILE_PATH_AFTER_ZIP " + file_path
		run_job_item(job_item, timeout)
	os.remove(zip_file_path)

def create_job_items_from_directory(job_item, dir_path):
	items_log.info("Creating job items from directory")
	fileslist = []
	for (dirpath, dirnames, filenames) in os.walk(dir_path):
		for f in filenames:
			fileslist.append({
				"filename": f,
				"file_path": os.path.join(dirpath,f),				
			})
	for f in fileslist:
		s3.upload_file(f['filename'], f['file_path'], S3_WORKING_INPUT_BUCKET)
		create_job_item(job_item['job_id'], f['filename'], sqs.get_queue(SQS_JOB_ITEMS_QUEUE))

def create_job_item(job_id, filename, queue):
	job = Job.query.get(int(job_id))
	job_item_doc = build_job_item_doc(job, filename)
	store_job_item_doc(job_item_doc)
	add_job_item_to_queue(job_item_doc.job_item_key, queue)
	return get_job_item_doc(job_item_doc.job_item_key)

def get_job_item_download_url(job_item_key):
	job_item = get_job_item_doc(job_item_key)
	s3_key = job_item['output_dir'] + "/" + job_item['output_filename']
	s3_conn = s3.S3Connection(VAA3D_USER_AWS_ACCESS_KEY, VAA3D_USER_AWS_SECRET_KEY)
	link_expiry_secs = 3600 # 1 hour
	return s3.get_download_url(s3_conn, S3_OUTPUT_BUCKET, s3_key, link_expiry_secs)

def build_job_item_doc(job, input_filename):
	output_filename = input_filename + job.output_file_suffix
	job_item = JobItemDocument(job.job_id, input_filename, output_filename, 
		job.output_dir, job.plugin, job.method)
	return job_item

def store_job_item_doc(job_item_doc):
	conn = dynamo.get_connection()
	table = dynamo.get_table(conn, DYNAMO_JOB_ITEMS_TABLE)
	dynamo.insert(table, job_item_doc.as_dict())

def get_job_item_doc(job_item_key):
	# This can be modified like a dictionary, and saved to Dynamo
	conn = dynamo.get_connection()
	table = dynamo.get_table(conn, DYNAMO_JOB_ITEMS_TABLE)
	return dynamo.get(table, job_item_key)

def save_job_item(job_item):
	conn = dynamo.get_connection()
	table = dynamo.get_table(conn, DYNAMO_JOB_ITEMS_TABLE)
	table.put_item(Item=job_item)

def add_job_item_to_queue(job_item_key, queue):
	message_id = sqs.send_message(queue, job_item_key, msg_dict={
		"job_item_key" : { "StringValue" : job_item_key, "DataType" : "String"},
		"job_type" : { "StringValue" : PROCESS_JOB_ITEM_TASK, "DataType" : "String"}
		})
	return message_id

def convert_dynamo_job_item_to_dict(dynamo_item):
	item_dict = {}
	for key in dynamo_item:
		if type(dynamo_item[key]) == Decimal:
			item_dict[key] = int(dynamo_item[key])
		else:
			item_dict[key] = dynamo_item[key]
	return item_dict
