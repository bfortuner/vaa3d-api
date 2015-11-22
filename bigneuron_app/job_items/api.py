from bigneuron_app import application
from bigneuron_app.job_items import job_item_manager
from flask import jsonify, request

@application.route('/job_item_url/<job_item_id>', methods=['GET'])
def get_job_item_url(job_item_id):
	download_url = job_item_manager.get_job_item_download_url(job_item_id)
	return jsonify( {'url' : download_url} )