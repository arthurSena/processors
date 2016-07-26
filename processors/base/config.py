# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import logging
from logging.handlers import SysLogHandler
from dotenv import load_dotenv
load_dotenv('.env')


# Storage

WAREHOUSE_URL = os.environ['WAREHOUSE_URL']
DATABASE_URL = os.environ['DATABASE_URL']

# Logging

logging.basicConfig(level=logging.DEBUG)
if os.environ.get('LOGGING_URL', None):
    root_logger = logging.getLogger()
    host, port = os.environ['LOGGING_URL'].split(':')
    syslog_handler = SysLogHandler(address=(host, int(port)))
    syslog_handler.setLevel(logging.INFO)
    root_logger.addHandler(syslog_handler)

# OSF

OSF_URL = os.environ.get('OSF_URL', None)
OSF_KEY = os.environ.get('OSF_KEY', None)
OSF_NAMESPACE = os.environ.get('OSF_NAMESPACE', None)
