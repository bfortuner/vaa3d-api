from bigneuron_app import application
from bigneuron_app.jobs import job_manager
from bigneuron_app.jobs.constants import JOB_TYPES, JOB_TYPE_PLUGINS, PLUGINS
from bigneuron_app.users import user_manager
from flask import jsonify, request

@application.route('/input_filenames', methods=['GET'])
@application.route('/input_filenames/<user_id>', methods=['GET'])
def get_available_input_filenames(user_id=None):
	application.logger.info("Getting input filenames" + str(user_id))
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
	application.logger.info("creating job " + str(request.json))
	data = request.json
	user = user_manager.get_or_create_user(data['emailAddress'])
	job_id = job_manager.create_job(user, data)
	return jsonify( {'job_id' : job_id} )

@application.route('/job/<job_id>', methods=['GET'])
def get_job(job_id):
	application.logger.info("Getting Job by Id: " + str(job_id))
	job = job_manager.get_job(job_id)
	return jsonify( {'job' : job} )

@application.route('/job_items/<int:job_id>', methods=['GET'])
def get_job_items(job_id):
	job_items = job_manager.get_job_items(job_id)
	application.logger.info("Getting Job Items: " + str(request.json))
	return jsonify( {'job_items' : job_items} )
