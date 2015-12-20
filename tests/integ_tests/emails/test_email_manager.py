from bigneuron_app.jobs.models import Job
from bigneuron_app.emails.email_manager import *

def test_email_manager():
	job = Job.query.first()
	print get_job_complete_template(job)
	send_job_created_email(job)
	send_job_complete_email(job)