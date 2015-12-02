from bigneuron_app import application
from bigneuron_app.users import user_manager
from flask import jsonify, request

@application.route('/get_or_create_user', methods=['POST'])
def get_or_create_user():
	application.logger.info("Getting or Creating new user")
	email = request.json['email']
	user = user_manager.get_or_create_user(email)
	return jsonify( {'user_id' : user.id} )
