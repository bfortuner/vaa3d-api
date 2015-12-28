from bigneuron_app import config
from bigneuron_app.clients.constants import AWS_IAM_USER_LOGIN_LINK

WEBSITE_URL=config.WEBSITE_URL

ADMIN_EMAIL='bfortuner@gmail.com'
DEV_EMAIL='bfortuner@gmail.com'
ERRORS_EMAIL=ADMIN_EMAIL

HEADER="<html>"
FOOTER="</html>"
CREATE_JOB_CONFIRMATION_TEMPLATE="""<p>Hello,</p>
<p>Your new Vaa3D job is running! You will receive a confirmation email when your job completes. 
Use the output link below to check the status of your job.</p>
<p>Job Status: %s</p>
<p><a href="%s">View Output Files</a></p>
<p>Thanks,<br>
Vaa3D Team</p>
"""
CREATE_JOB_CONFIRMATION_TEMPLATE = HEADER + CREATE_JOB_CONFIRMATION_TEMPLATE + FOOTER

COMPLETE_JOB_CONFIRMATION_TEMPLATE="""<p>Hello,</p>
<p>Your new Vaa3D job is complete! Please use the download link below OR 
log into the AWS S3 <b>vaa3d-output</b> bucket to view your files.</p>
<p>Job Status: %s</p>
<p><a href="%s">View Output Files</a></p>
<p><a href="%s">Login to S3</a> (email vaa3dapi@gmail.com for password)</p>
<p>Thanks,<br>
Vaa3D Team</p>
"""
COMPLETE_JOB_CONFIRMATION_TEMPLATE = HEADER + COMPLETE_JOB_CONFIRMATION_TEMPLATE + FOOTER

CREATE_JOB_CONFIRMATION ={
	'subject' : 'Your New Vaa3D Job',
	'body' : CREATE_JOB_CONFIRMATION_TEMPLATE
}

COMPLETE_JOB_CONFIRMATION ={
	'subject' : 'Your Vaa3D Job is Complete!',
	'body' : COMPLETE_JOB_CONFIRMATION_TEMPLATE
}