from bigneuron_app.job_items.tasks import *
from bigneuron_app.clients.constants import *
from bigneuron_app.jobs.constants import OUTPUT_FILE_SUFFIXES, VAA3D_DEFAULT_PLUGIN


def test_process_next_job_item():
	queue = sqs.get_queue(SQS_JOB_ITEMS_QUEUE)
	job = Job(1, 1, "mytestdir", VAA3D_DEFAULT_PLUGIN, VAA3D_DEFAULT_FUNC, 1, OUTPUT_FILE_SUFFIXES[VAA3D_DEFAULT_PLUGIN])
	db.add(job)
	db.commit()
	job_item = job_item_manager.create_job_item(job.job_id, VAA3D_TEST_INPUT_FILE_1, queue)
	process_next_job_item()
