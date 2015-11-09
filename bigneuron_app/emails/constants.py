from bigneuron_app.clients.constants import AWS_IAM_USER_LOGIN_LINK

ADMIN_EMAIL='vaa3dapi@gmail.com'

CREATE_JOB_CONFIRMATION_TEMPLATE="""<p>Hello,</p>
<p>Your new Vaa3d job is running! You will receive a confirmation email when your job completes.</p>
<p>Thanks,<br>
Vaa3D Team</p>
"""

COMPLETE_JOB_CONFIRMATION_TEMPLATE="""<p>Hello,</p>
<p>Your new Vaa3d job is complete! Please log in to AWS S3 using the link below. You can download your output files from the vaa3d-output bucket</p>
<p><a href="%s">Login To AWS S3</a></p>
<p>Thanks,<br>
Vaa3D Team</p>
""" % AWS_IAM_USER_LOGIN_LINK

CREATE_JOB_CONFIRMATION ={
	'subject' : 'Your New Vaa3d Job',
	'body' : "<html>" + CREATE_JOB_CONFIRMATION_TEMPLATE + "</html>"
}

COMPLETE_JOB_CONFIRMATION ={
	'subject' : 'Your Vaa3d Job is Complete!',
	'body' : "<html>" + COMPLETE_JOB_CONFIRMATION_TEMPLATE + "</html>"
}