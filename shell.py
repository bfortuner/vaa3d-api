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