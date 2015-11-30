import os, sys
import shutil
import logging
from logging import Formatter
from bigneuron_app.emails.constants import DEV_EMAIL, ERRORS_EMAIL
from bigneuron_app.utils.constants import LOG_LEVEL, LOG_FILE_PATH, LOG_INTERVAL_TYPE, LOG_BACKUP_INCR, LOG_INTERVAL

from logging.handlers import TimedRotatingFileHandler
from logging.handlers import SMTPHandler

def create_log_dir(log_file_path):
	if not os.path.exists(os.path.dirname(log_file_path)):
		os.makedirs(os.path.dirname(log_file_path))

def get_mail_handler(log_level=LOG_LEVEL):
	mail_handler = SMTPHandler('localhost', # Mail host,
							ERRORS_EMAIL, # From Email 
							[DEV_EMAIL], # To email 
							'ERROR - %s' % str(__name__)
	)
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
	rotating_file_handler.suffix = "%Y-%m-%d_%H:%M:%S" 
	return rotating_file_handler

def get_logger(name, log_level=LOG_LEVEL):
	logger = logging.getLogger(name)
	logger.setLevel(log_level)
	logger.addHandler(get_rotating_file_handler(name))
	return logger

