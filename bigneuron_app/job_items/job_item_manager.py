import sys
import zipfile
import shutil

from bigneuron_app import db
from bigneuron_app.job_items.models import JobItem, JobItemStatus, JobItemDocument
from bigneuron_app.jobs.models import Job
from bigneuron_app.clients import s3, vaa3d
from bigneuron_app.clients.constants import *
from bigneuron_app.clients.constants import S3_INPUT_BUCKET, S3_OUTPUT_BUCKET
from bigneuron_app.clients.constants import VAA3D_USER_AWS_ACCESS_KEY, VAA3D_USER_AWS_SECRET_KEY
from bigneuron_app.clients.constants import DYNAMO_JOB_ITEMS_TABLE
from bigneuron_app.utils import zipper
from bigneuron_app.clients import dynamo


def process_next_job_item():
	new_job_status = JobItemStatus.query.filter_by(status_name="CREATED").first()
	job_item = JobItem.query.filter_by(status_id=new_job_status.id).order_by(JobItem.created).first()
	if job_item is None: 
		print "No job items found in Queue"
		return
	print "Found new job_item"
	job_item.status_id = get_job_item_status_id("IN_PROGRESS")
	db.session.commit()
	local_file_path = os.path.abspath(job_item.filename)
	bucket_name = s3.get_bucket_name_from_filename(job_item.filename, 
		[S3_INPUT_BUCKET, S3_WORKING_INPUT_BUCKET])
	s3.download_file(job_item.filename, local_file_path, bucket_name)
	run_job_item(job_item)

def run_job_item(job_item):
	local_file_path = os.path.abspath(job_item.filename)
	try:
		if zipper.is_zip_file(local_file_path):
			process_zip_file(job_item, local_file_path)
		else:
			process_non_zip_file(job_item)
		job_item.status_id = get_job_item_status_id("COMPLETE")
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

def process_non_zip_file(job_item):
	vaa3d_job = vaa3d.build_vaa3d_job(job_item)
	vaa3d.run_job(vaa3d_job)
	s3_key = job_item.job.output_dir + "/" + vaa3d_job.output_filename
	s3.upload_file(s3_key, vaa3d_job.output_file_path, S3_OUTPUT_BUCKET)
	vaa3d.cleanup(vaa3d_job.input_file_path, vaa3d_job.output_file_path)

def process_zip_file(job_item, zip_file_path):
	"""
	Unzips a compressed file
	Creates new job_item record(s)
	Uploads new uncompressed file(s) to s3
	"""
	output_dir = os.path.dirname(zip_file_path)
	zip_archive = zipfile.ZipFile(zip_file_path, "r")
	filenames = zip_archive.namelist()
	if len(filenames) > 1:
		output_dir = os.path.join(output_dir, zip_file_path[:zip_file_path.find(zipper.ZIP_FILE_EXT)])
		zipper.expand_zip_archive(zip_archive, output_dir)
		zip_archive.close()
		create_job_items_from_directory(job_item, output_dir)
		shutil.rmtree(output_dir)
	else:
		filename = filenames[0]
		file_path = os.path.join(output_dir, filename)
		zipper.extract_file_from_archive(zip_archive, filename, file_path)
		zip_archive.close()

		new_job_item = create_job_item(job_item.job.job_id, filename, file_path)
		run_job_item(new_job_item)
	os.remove(zip_file_path)

def create_job_items_from_directory(job_item, dir_path):
	fileslist = []
	for (dirpath, dirnames, filenames) in os.walk(dir_path):
		for f in filenames:
			fileslist.append({
				"filename": f,
				"file_path": os.path.join(dirpath,f),				
			})
	for f in fileslist:
		s3.upload_file(f['filename'], f['file_path'], S3_WORKING_INPUT_BUCKET)
		create_job_item(job_item.job.job_id, f['filename'], f['file_path'])

def create_job_item(job_id, filename, file_path):
	job_item = JobItem(job_id, filename, 1)
	db.session.add(job_item)
	db.session.commit()
	return job_item

def get_job_item_download_url(job_item_id):
	job_item = JobItem.query.get(job_item_id)
	s3_conn = s3.S3Connection(VAA3D_USER_AWS_ACCESS_KEY, VAA3D_USER_AWS_SECRET_KEY)
	link_expiry_secs = 3600 # 1 hour
	return s3.get_download_url(s3_conn, S3_OUTPUT_BUCKET, job_item.get_output_s3_key(), link_expiry_secs)

def build_job_item_doc(job, input_filename):
	output_filename = input_filename + job.output_file_suffix
	job_item = JobItemDocument(job.job_id, input_filename, output_filename, 
		job.output_dir, job.plugin, job.method)
	return job_item

def create_job_item_doc(job_item_doc):
	conn = dynamo.get_connection()
	table = dynamo.get_table(conn, DYNAMO_JOB_ITEMS_TABLE)
	dynamo.insert(table, job_item_doc.as_dict())

def get_job_item_doc(job_item_id):
	# This can be modified like a dictionary, and saved to Dynamo
	conn = dynamo.get_connection()
	table = dynamo.get_table(conn, DYNAMO_JOB_ITEMS_TABLE)
	return dynamo.get(table, job_item_id)
	


## Unit Tests ##

def test_all():
	from bigneuron_app.utils import id_generator
	input_filename = id_generator.generate_job_item_id()[:10] + ".tif"
	conn = dynamo.get_connection()
	table_name = id_generator.generate_job_item_id()[:10] + "_table"
	table = dynamo.create_table(conn, table_name, 'job_item_id', 'S')
	table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

	job = Job(1, 1, "mytestdir", VAA3D_DEFAULT_PLUGIN, VAA3D_DEFAULT_FUNC, 1, VAA3D_DEFAULT_OUTPUT_SUFFIX)
	db.session.add(job)
	db.session.commit()
	print "job_id: " + str(job.job_id)
	job_item_doc = build_job_item_doc(job, input_filename)
	print job_item_doc.as_dict()
	create_job_item_doc(job_item_doc)
	print job_item_doc.job_item_id
	job_item_record = get_job_item_doc(job_item_doc.job_item_id)
	print job_item_record

	print job_item_record['channel'], job_item_record['input_filename']

	dynamo.drop_table(conn, table_name)


