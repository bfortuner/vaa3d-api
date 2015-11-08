from bigneuron_app import application
from bigneuron_app.jobs import job_manager
from bigneuron_app.users import user_manager
from flask import jsonify, request

@application.route('/input_filenames', methods=['GET'])
@application.route('/input_filenames/<user_id>', methods=['GET'])
def get_available_input_filenames(user_id=None):
	filenames = job_manager.get_user_input_filenames(user_id)
	return jsonify( {'filenames' : filenames} )

@application.route('/create_job', methods=['POST'])
def create_job():
	filenames = request.json['filenames']
	email = request.json['email']
	user = user_manager.get_or_create_user(email)
	job_id = job_manager.create_job(filenames, user)
	return jsonify( {'job_id' : job_id} )


