from __future__ import absolute_import, unicode_literals
from celery import shared_task
import requests
from requests.auth import HTTPBasicAuth
from mikrokridit.celery import app
from datetime import datetime, timedelta
from celery.utils.log import get_task_logger
import os
from mkridit import sendmail


logger = get_task_logger(__name__)

@shared_task()
def check_endpoints():
    os.system("python manage.py collect_data")


@shared_task()
def send_email():
    sendmail.send()
    
    