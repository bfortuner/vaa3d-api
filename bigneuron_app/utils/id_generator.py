import uuid


JOB_ITEM_ID_PREFIX="JI"
JOB_ID_PREFIX="JO"

def generate_job_item_id():
	return JOB_ITEM_ID_PREFIX + str(uuid.uuid4()).upper().replace('-','') + '01'

def generate_job_id():
	# currently using SQLAlchemy auto-increment id
	pass


## Unit Tests ##

def test_all():
	job_item_id = generate_job_item_id()
	print job_item_id