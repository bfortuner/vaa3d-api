#!/usr/bin/env python
import os
import readline
from pprint import pprint

from flask import *
from bigneuron_app import *

os.environ['PYTHONINSPECT'] = 'True'

from bigneuron_app.utils import zipper
from bigneuron_app.clients import vaa3d
from bigneuron_app.job_items import job_item_manager
from bigneuron_app.job_items.models import JobItem

#vaa3d.test_plugins()
vaa3d.test_single_plugin()