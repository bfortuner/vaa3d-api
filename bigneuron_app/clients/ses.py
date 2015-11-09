import boto.ses
from bigneuron_app.clients.constants import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION
from bigneuron_app.emails.constants import ADMIN_EMAIL


def get_connection():
	"""
	For EC2 hosts this is managed by roles
	IAM users must add the correct AWS tokens to their .bash_profile
	"""
	try:
		return boto.ses.connect_to_region()
	except:
		return boto.ses.connect_to_region(AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY, 
			aws_secret_access_key=AWS_SECRET_KEY)

def send_address_verification_email(email_address):
	print "Sending address verification email: %s" % email_address
	get_connection().verify_email_address(email_address)

def is_email_address_verified(email_address):
	print "Attempting to verify email address: %s" % email_address
	verified_emails_resp = get_connection().list_verified_email_addresses()['ListVerifiedEmailAddressesResponse']
	verified_emails = verified_emails_resp['ListVerifiedEmailAddressesResult']['VerifiedEmailAddresses']
	for email in verified_emails:
		if email == email_address:
			return True
	return False

def send_email(subject, body, to_email, from_email=ADMIN_EMAIL):
	print "Attempting to send email to %s from %s" % (to_email, from_email)
	get_connection().send_email(from_email, subject, body, [to_email], html_body=body)
	print "Sent email to %s from %s" % (to_email, from_email)

def test_ses_client():
	TEST_TO_EMAIL='bfortuner@gmail.com'
	#send_address_verification_email(TEST_TO_EMAIL)
	print is_email_address_verified(TEST_TO_EMAIL) == True
	print is_email_address_verified('fake_email@address.com') == False
	send_email('TEST', 'TEST BODY', TEST_TO_EMAIL)