from bigneuron_app.emails.constants import *
from bigneuron_app.users import user_manager
from bigneuron_app.clients import ses
from bigneuron_app.jobs.models import Job
from bigneuron_app.clients.constants import AWS_IAM_USER_LOGIN_LINK


def send_job_created_email(job):
	user = user_manager.get_user_by_id(job.user_id)
	ses.send_email(CREATE_JOB_CONFIRMATION['subject'],
		CREATE_JOB_CONFIRMATION['body'], user.email)

def send_job_complete_email(job):
	user = user_manager.get_user_by_id(job.user_id)
	body = get_job_complete_template(job)
	ses.send_email(COMPLETE_JOB_CONFIRMATION['subject'],
		body, user.email)

def get_job_complete_template(job):
	output_files_link = WEBSITE_URL + '/#/view_job_items/' + str(job.job_id) 
	return COMPLETE_JOB_CONFIRMATION['body'] % (job.job_status.status_name, 
		output_files_link, AWS_IAM_USER_LOGIN_LINK)

def test_email_manager():
	job = Job.query.first()
	print get_job_complete_template(job)
	send_job_created_email(job)
	send_job_complete_email(job)
