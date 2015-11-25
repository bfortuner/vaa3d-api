from datetime import datetime
from bigneuron_app import db
from bigneuron_app.utils import id_generator

class JobItem(db.Model):
	__tablename__ = 'job_items'
	job_item_id = db.Column(db.Integer, primary_key=True)
	job_item_key = db.Column(db.String(128), nullable=False)
	job_id = db.Column(db.Integer, db.ForeignKey('jobs.job_id'), nullable=False)
	filename = db.Column(db.String(128), nullable=False)
	status_id = db.Column(db.Integer, db.ForeignKey('job_item_status_types.id'), nullable=False)
	created = db.Column(db.DateTime, default=db.func.now())
	last_updated = db.Column(db.DateTime, onupdate=db.func.now())
	job = db.relationship('Job', backref=db.backref('job_items', lazy='dynamic'))
	job_item_status = db.relationship('JobItemStatus', backref=db.backref('job_items', lazy='dynamic'))

	def get_output_filename(self):
		return self.filename + self.job.output_file_suffix

	def get_output_s3_key(self):
		return self.job.output_dir + "/" + self.get_output_filename()

	def __init__(self, job_id, job_item_key, filename, status_id):
		self.job_id = job_id
		self.job_item_key = job_item_key
		self.filename = filename
		self.status_id = status_id

	def __repr__(self):
		return '<JobItem %r>' % self.filename

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class JobItemStatus(db.Model):
	__tablename__ = 'job_item_status_types'
	id = db.Column(db.Integer, primary_key=True)
	status_name = db.Column(db.String(32), nullable=False)
	description = db.Column(db.String(128))

	__table_args__ = (
        db.UniqueConstraint("id", "status_name"),
    )

	def __init__(self, status_name):
		self.status_name = status_name

	def __repr__(self):
		return '<JobItemStatus %r>' % self.status_name


# DynamoDB JobItem JSON

class JobItemDocument():

	def __init__(self, job_id, input_filename, output_filename, 
		output_dir, plugin, method, channel=1, status_id=1):
		self.job_item_key = id_generator.generate_job_item_id()
		self.job_id = job_id
		self.input_filename = input_filename
		self.output_filename = output_filename
		self.output_dir = output_dir
		self.plugin = plugin
		self.method = method
		self.channel = channel
		self.status_id = status_id

	def __repr__(self):
		return '<JobItemDocument %r>' % self.input_filename

	def as_dict(self):
		return self.__dict__



# key = job_item_id
# data = {
# 	"job_item_key" : job_item_id,
# 	"job_id" : job_id,
# 	"input_filename" : input_filename,
# 	"output_filename" : output_filename,
# 	"output_dir" : output_dir,
# 	"status_id" : status_id,
# 	"plugin" : plugin,
# 	"method" : method,
# 	"channel" : channel,
# 	"created" : created
# }