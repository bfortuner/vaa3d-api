from bigneuron_app.emails.constants import *
from bigneuron_app.users import user_manager
from bigneuron_app.clients import ses
from bigneuron_app.jobs.models import Job


def send_job_created_email(job):
	user = user_manager.get_user_by_id(job.user_id)
	ses.send_email(CREATE_JOB_CONFIRMATION['subject'],
		CREATE_JOB_CONFIRMATION['body'], user.email)

def send_job_complete_email(job):
	user = user_manager.get_user_by_id(job.user_id)
	ses.send_email(COMPLETE_JOB_CONFIRMATION['subject'],
		COMPLETE_JOB_CONFIRMATION['body'], user.email)

def test_email_manager():
	job = Job.query.first()
	send_job_created_email(job)
	send_job_complete_email(job)
