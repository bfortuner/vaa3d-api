import time
from datetime import datetime
from bigneuron_app.utils import id_generator
from bigneuron_app.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func


class JobItemStatus(Base):
	__tablename__ = 'job_item_status_types'
	id = Column(Integer, primary_key=True)
	status_name = Column(String(32), nullable=False)
	description = Column(String(128))

	__table_args__ = (
        UniqueConstraint("id", "status_name"),
    )

	def __init__(self, status_name):
		self.status_name = status_name

	def __repr__(self):
		return '<JobItemStatus %r>' % self.status_name


# DynamoDB JobItem JSON
class JobItemDocument():

	def __init__(self, job_id, input_filename, output_filename, 
		output_dir, plugin, method, channel=1, status_id=1, attempts=0):
		self.job_item_key = id_generator.generate_job_item_id()
		self.job_id = int(job_id)
		self.input_filename = input_filename
		self.output_filename = output_filename
		self.output_dir = output_dir
		self.plugin = plugin
		self.method = method
		self.channel = int(channel)
		self.status_id = int(status_id)
		self.attempts = int(attempts)
		self.creation_time = int(time.time()) #UTC = PST + 8

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