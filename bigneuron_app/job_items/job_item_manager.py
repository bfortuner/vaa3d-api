import sys
import zipfile
import shutil

from bigneuron_app import db
from bigneuron_app.job_items.models import JobItem, JobItemStatus
from bigneuron_app.clients import s3, vaa3d
from bigneuron_app.clients.constants import *
from bigneuron_app.utils import zipper 


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
