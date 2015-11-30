import os, sys
import shutil
import logging
from logging import Formatter
from bigneuron_app.clients import ses
from bigneuron_app.emails.constants import DEV_EMAIL, ERRORS_EMAIL
from bigneuron_app.utils.constants import *

from logging.handlers import TimedRotatingFileHandler
from logging.handlers import SMTPHandler

def create_log_dir(log_file_path):
	if not os.path.exists(os.path.dirname(log_file_path)):
		os.makedirs(os.path.dirname(log_file_path))

class SESHandler(SMTPHandler):
	""" 
	Send an email using BOTO SES.
	"""
	def emit(self, record):
		conn = ses.get_connection()
		conn.send_email(self.fromaddr, self.subject, self.format(record), self.toaddrs)

def get_mail_handler(name, log_level=MAIL_LOG_LEVEL):
	mail_handler = SESHandler(mailhost='', fromaddr=ERRORS_EMAIL, toaddrs=[DEV_EMAIL], 
		subject='ERROR - %s' % name)
	mail_handler.setLevel(log_level)
	mail_handler.setFormatter(Formatter('''
	Message type:       %(levelname)s
	Location:           %(pathname)s:%(lineno)d
	Module:             %(module)s
	Function:           %(funcName)s
	Time:               %(asctime)s

	Message:

	%(message)s
	'''))
	return mail_handler

def get_rotating_file_handler(logger_name, log_level=LOG_LEVEL):
	logger_path = LOG_FILE_PATH + '/' + logger_name + '.log'
	create_log_dir(logger_path)
	rotating_file_handler = TimedRotatingFileHandler(logger_path, 
		when=LOG_INTERVAL_TYPE, interval=LOG_INTERVAL, backupCount=LOG_BACKUP_INCR)
	rotating_file_handler.setFormatter(Formatter('''[%(levelname)s] %(asctime)s - %(module)s.%(funcName)s line %(lineno)d
	  %(message)s'''
	))
	rotating_file_handler.setLevel(log_level)
	rotating_file_handler.suffix = "%Y-%m-%d" #_%H:%M:%S" 
	return rotating_file_handler

def get_logger(name, log_level=LOG_LEVEL):
	logger = logging.getLogger(name)
	logger.setLevel(log_level)
	logger.addHandler(get_rotating_file_handler(name, LOG_LEVEL))
	logger.addHandler(get_mail_handler(name, MAIL_LOG_LEVEL))
	return logger

