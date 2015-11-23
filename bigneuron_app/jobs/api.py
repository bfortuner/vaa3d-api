from bigneuron_app import application
from bigneuron_app.jobs import job_manager
from bigneuron_app.jobs.constants import JOB_TYPES, JOB_TYPE_PLUGINS, PLUGINS
from bigneuron_app.users import user_manager
from flask import jsonify, request

@application.route('/input_filenames', methods=['GET'])
@application.route('/input_filenames/<user_id>', methods=['GET'])
def get_available_input_filenames(user_id=None):
	filenames = job_manager.get_user_input_filenames(user_id)
	return jsonify( {'filenames' : filenames} )

@application.route('/plugins', methods=['GET'])
def get_job_type_plugins():
	return jsonify({
		'job_types' : JOB_TYPES,
		'job_type_plugins' : JOB_TYPE_PLUGINS,
		'plugins' : PLUGINS
	})

@application.route('/create_job', methods=['POST'])
def create_job():
	print "creating job " + str(request.json)
	data = request.json
	user = user_manager.get_or_create_user(data['emailAddress'])
	job_id = job_manager.create_job(user, data)
	return jsonify( {'job_id' : job_id} )

@application.route('/job_items/<job_id>', methods=['GET'])
def get_job_items(job_id):
	job_items = job_manager.get_job_items(job_id)
	print job_items
	return jsonify( {'job_items' : job_items} )