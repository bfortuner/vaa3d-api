#!/usr/bin/env python
import os
import time
import readline
from pprint import pprint

from flask import *
from bigneuron_app import *

os.environ['PYTHONINSPECT'] = 'True'

from bigneuron_app.emails import email_manager
from bigneuron_app.clients.constants import S3_OUTPUT_BUCKET
from bigneuron_app.clients import s3
from bigneuron_app.clients import sqs
from bigneuron_app.clients import dynamo
from bigneuron_app.utils import zipper
from bigneuron_app.clients import vaa3d
from bigneuron_app.jobs import job_manager
from bigneuron_app.job_items import job_item_manager
from bigneuron_app.utils import id_generator



#email_manager.test_email_manager()

#vaa3d.test_plugins()
#vaa3d.test_single_plugin()

#job_manager.test_get_job_items()
#print s3.get_download_url('vaa3d-output', 'Mynewtest/smalltest.tif_x72_y57_z64_app2.swc', 3600)
#dynamo.test_all()
#id_generator.test_all()

#job_item_manager.test_all()
#job_item_manager.test_process_next_job_item()
#sqs.test_all()
#sqs.test_clear_queue()
#sqs.test_get_queue()
#sqs.test_get_queue_name()

#job_item_manager.test_process_next_job_item()

job_manager.test_get_job_items()
#job_item_manager.test_convert_dynamo_item_to_dict()