from bigneuron_app import db
from bigneuron_app.utils import zipper

class Job(db.Model):
	__tablename__ = 'jobs'
	job_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	status_id = db.Column(db.Integer, db.ForeignKey('job_status_types.id'), nullable=False)
	output_dir = db.Column(db.String(128), nullable=False)
	plugin = db.Column(db.String(128), nullable=False)
	method = db.Column(db.String(128), nullable=False)
	channel = db.Column(db.Integer, nullable=False)
	output_file_suffix = db.Column(db.String(128), nullable=False)
	created = db.Column(db.DateTime, default=db.func.now())
	last_updated = db.Column(db.DateTime, onupdate=db.func.now())
	job_status = db.relationship('JobStatus', backref=db.backref('jobs', lazy='dynamic'))
	user = db.relationship('User', backref=db.backref('jobs', lazy='dynamic'))

	def __init__(self, user_id, status_id, output_dir, plugin, method, channel, output_file_suffix):
		self.user_id = user_id
		self.status_id = status_id
		self.output_dir = output_dir
		self.plugin = plugin
		self.method = method
		self.channel = channel
		self.output_file_suffix = output_file_suffix

	def get_output_s3_key(self):
		return self.output_dir + zipper.ZIP_FILE_EXT

	def __repr__(self):
		return '<Job %r>' % self.job_id

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class JobStatus(db.Model):
	__tablename__ = 'job_status_types'
	id = db.Column(db.Integer, primary_key=True)
	status_name = db.Column(db.String(32), nullable=False)
	description = db.Column(db.String(128))	

	__table_args__ = (
        db.UniqueConstraint("id", "status_name"),
    )

	def __init__(self, status_name):
		self.status_name = status_name

	def __repr__(self):
		return '<JobStatus %r>' % self.status_name