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
	print "creating job " + str(request.json)
	data = request.json
	user = user_manager.get_or_create_user(data['emailAddress'])
	job_id = job_manager.create_job(user, data)
	return jsonify( {'job_id' : job_id} )