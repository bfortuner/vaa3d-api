from bigneuron_app import application
from bigneuron_app.jobs import manager
from flask import jsonify, request

@application.route('/input_filenames', methods=['GET'])
@application.route('/input_filenames/<user_id>', methods=['GET'])
def get_available_input_filenames(user_id=None):
	filenames = manager.get_user_input_filenames(user_id)
	return jsonify( {'filenames' : filenames} )

@application.route('/create_job', methods=['POST'])
def create_job():
	filenames = request.json['filenames']
	user_email = request.json['user_email']
	job_id = manager.create_job(filenames, user_email)
	return jsonify( {'job_id' : job_id} )


