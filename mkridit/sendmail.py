from datetime import timedelta
import smtplib, ssl
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from statistics import mode
from urllib import request
from email import encoders
from email.mime.base import MIMEBase
import requests

import logging

# Create a logger for this file
logger = logging.getLogger(__file__)


def send():
    from mkridit.models import SMTP
    obj = SMTP.objects.last()
    if not obj:
        return
    
    send_mail_now(obj.mail,obj.to,obj.password,obj.subject,obj.signature,obj.server,obj.port)


from django.core.mail.backends import smtp

class CustomEmailBackend(smtp.EmailBackend):
  def __init__(self, *args, **kwargs):
      kwargs.setdefault('timeout', 3)
      super(CustomEmailBackend, self).__init__(*args, **kwargs)
      
def custom_email_backend():
    from mkridit.models import SMTP
    obj = SMTP.objects.last()
    if not obj:
        return
    tsl, ssl = False, True
    backend = CustomEmailBackend(obj.server, obj.port, obj.mail,
                                obj.password, tsl, False, ssl)
    return backend

def send_email(uploaded_file, subject, content, contact_email, to):
    from django.core.mail import EmailMessage
    ...
    logger.info(f'{to},EMILLER')
    email = EmailMessage(
        subject,
        content,
        contact_email,
        to,
        connection=custom_email_backend(),
        headers={'Reply-To': contact_email}
    )
    email.attach(uploaded_file.name, uploaded_file.read(), None)
    email.send()


def send_mail_now(sender,to,password,subject,signature,server,port):
    import datetime
    from mkridit.api.views import ExportAPI
    from datetime import timedelta

    e = datetime.datetime.now()
    d = e - timedelta(days=1)
    e = str(e)
    d = str(d)
    
    cr_time = e.split(" ")[0]
    bf_time = d.split(" ")[0]


    logger.info(f'{bf_time} bff timee')
    logger.info(f'{cr_time} this crtimee')
    sender_email = sender
    receiver_email = to
    password = password

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email
    data = requests.get(f'http://127.0.0.1:8000/api/report/?date[]={bf_time}&date[]={cr_time}')

    if data:
        data = data.json()
        data = data.get('results')
        if data :
            url,file = ExportAPI.export(data,"csv")     
            with open(file, "rb") as attachment:
                send_email(attachment, subject, signature, sender_email, receiver_email)