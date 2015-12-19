#!/usr/bin/env python
import os
import time
import readline
from pprint import pprint

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
from bigneuron_app.utils import id_generator, command

import bigneuron_app.job_items.tasks as job_item_tasks
import bigneuron_app.jobs.tasks as job_tasks

import task_runner

import bigneuron_app.utils.logger as logger

#email_manager.test_email_manager()

#vaa3d.test_single_plugin_local()
#vaa3d.cleanup_all_filename_not_found()

#job_manager.test_get_job_items()

#print s3.get_download_url('vaa3d-output', 'Mynewtest/smalltest.tif_x72_y57_z64_app2.swc', 3600)
#dynamo.test_all()

#job_item_manager.test_convert_dynamo_item_to_dict()
#job_item_manager.test_run_job_items()

job_item_tasks.test_process_next_job_item()

#job_tasks.poll_jobs_created_queue()
#job_tasks.poll_jobs_in_progress_queue()

#dynamo.test_scan_by_time()

#zipper.test_is_compressed_filename()


#command.test_command()


