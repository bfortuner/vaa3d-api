from bigneuron_app import db

class JobItem(db.Model):
	__tablename__ = 'job_items'
	job_item_id = db.Column(db.Integer, primary_key=True)
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

	def __init__(self, job_id, filename, status_id):
		self.job_id = job_id
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