from bigneuron_app.clients.ses import *

def test_ses_client():
	TEST_TO_EMAIL='bfortuner@gmail.com'
	#send_address_verification_email(TEST_TO_EMAIL)
	print is_email_address_verified(TEST_TO_EMAIL) == True
	print is_email_address_verified('fake_email@address.com') == False
	send_email('TEST', 'TEST BODY', TEST_TO_EMAIL)