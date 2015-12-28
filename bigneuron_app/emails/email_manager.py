from bigneuron_app import jobs_log
from bigneuron_app.emails.constants import *
from bigneuron_app.users import user_manager
from bigneuron_app.clients import ses
from bigneuron_app.jobs.models import Job
from bigneuron_app.clients.constants import AWS_IAM_USER_LOGIN_LINK


def send_job_created_email(job):
	jobs_log.info("Sending Job Created Email " + str(job.job_id))
	user = user_manager.get_user_by_id(job.user_id)
	body = get_job_created_template(job)
	ses.send_email(CREATE_JOB_CONFIRMATION['subject'],
		body, user.email)

def send_job_complete_email(job):
	jobs_log.info("Sending Job Complete Email " + str(job.job_id))
	user = user_manager.get_user_by_id(job.user_id)
	body = get_job_complete_template(job)
	ses.send_email(COMPLETE_JOB_CONFIRMATION['subject'],
		body, user.email)

def get_job_created_template(job):
	output_files_link = WEBSITE_URL + '/#/view_job_items/' + str(job.job_id) 
	return CREATE_JOB_CONFIRMATION['body'] % (job.job_status.status_name, 
		output_files_link)

def get_job_complete_template(job):
	output_files_link = WEBSITE_URL + '/#/view_job_items/' + str(job.job_id) 
	return COMPLETE_JOB_CONFIRMATION['body'] % (job.job_status.status_name, 
		output_files_link, AWS_IAM_USER_LOGIN_LINK)
