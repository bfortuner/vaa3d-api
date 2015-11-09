from bigneuron_app.clients.constants import AWS_IAM_USER_LOGIN_LINK

ADMIN_EMAIL='vaa3dapi@gmail.com'

HEADER="<html>"
FOOTER="</html>"
CREATE_JOB_CONFIRMATION_TEMPLATE="""<p>Hello,</p>
<p>Your new Vaa3D job is running! You will receive a confirmation email when your job completes.</p>
<p>Thanks,<br>
Vaa3D Team</p>
"""
CREATE_JOB_CONFIRMATION_TEMPLATE = HEADER + CREATE_JOB_CONFIRMATION_TEMPLATE + FOOTER

COMPLETE_JOB_CONFIRMATION_TEMPLATE="""<p>Hello,</p>
<p>Your new Vaa3D job is complete! Please log in to AWS S3 using the link below.
You can download your output files from the vaa3d-output bucket</p>
<p>Job Status: %s</p>
<p><a href="%s">Login To AWS S3</a></p>
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