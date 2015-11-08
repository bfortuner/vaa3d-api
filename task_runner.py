import sys
from bigneuron_app.jobs import job_manager
from bigneuron_app.job_items import job_item_manager

method = sys.argv[1]
print "Running " + method

if method == "process_jobs":
	job_manager.update_jobs_created()
	job_manager.update_jobs_in_progress()
elif method =="process_job_items":
	job_item_manager.process_next_job_item()