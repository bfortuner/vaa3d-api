from bigneuron_app.utils.id_generator import generate_job_item_id

def test_generate_job_item_id():
	job_item_id = generate_job_item_id()
	assert job_item_id is not None
	assert "-" not in job_item_id 