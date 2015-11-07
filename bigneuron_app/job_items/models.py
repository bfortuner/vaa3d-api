from bigneuron_app import db

class JobItem(db.Model):
	__tablename__ = 'job_items'
	job_item_id = db.Column(db.Integer, primary_key=True)
	job_id = db.Column(db.Integer, db.ForeignKey('jobs.job_id'), nullable=False)
	filename = db.Column(db.String(128), nullable=False)
	job_item_status_id = db.Column(db.Integer, 
		db.ForeignKey('job_item_status_types.id'), nullable=False)
	created = db.Column(db.DateTime, default=db.func.now())
	last_updated = db.Column(db.DateTime, onupdate=db.func.now())

	def __init__(self, job_id, filename, job_item_status_id):
		self.job_id = job_id
		self.filename = filename
		self.job_item_status_id = job_item_status_id

	def __repr__(self):
		return '<JobItem %r>' % self.job_item_id

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