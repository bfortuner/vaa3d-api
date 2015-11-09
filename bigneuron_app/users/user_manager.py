from bigneuron_app import db
from bigneuron_app.users.models import User
from bigneuron_app.users.constants import DEFAULT_IAM_USER

def get_or_create_user(email_address, iam_username=DEFAULT_IAM_USER):
	user = User.query.filter_by(email=email_address).first()
	if user is None:
		print "Creating new user"
		user = User(email_address, iam_username)
		db.session.add(user)
		db.session.commit()
	return user

def get_jobs_by_user(email_address):
	user = User.query.filter_by(email=email_address).first()
	jobs = user.jobs.all()
	return jobs

def get_user_by_id(user_id):
	return User.query.get(user_id)