from bigneuron_app.database import Base
from bigneuron_app.utils import zipper
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

class Job(Base):
	__tablename__ = 'jobs'
	job_id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
	status_id = Column(Integer, ForeignKey('job_status_types.id'), nullable=False)
	output_dir = Column(String(128), nullable=False)
	plugin = Column(String(128), nullable=False)
	method = Column(String(128), nullable=False)
	channel = Column(Integer, nullable=False)
	output_file_suffix = Column(String(128), nullable=False)
	created = Column(DateTime, default=func.now())
	last_updated = Column(DateTime, onupdate=func.now())
	job_status = relationship('JobStatus', backref=backref('jobs', lazy='dynamic'))
	user = relationship('User', backref=backref('jobs', lazy='dynamic'))

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


class JobStatus(Base):
	__tablename__ = 'job_status_types'
	id = Column(Integer, primary_key=True)
	status_name = Column(String(32), nullable=False)
	description = Column(String(128))	

	__table_args__ = (
        UniqueConstraint("id", "status_name"),
    )

	def __init__(self, status_name):
		self.status_name = status_name

	def __repr__(self):
		return '<JobStatus %r>' % self.status_name