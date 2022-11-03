from django.core.management.base import BaseCommand
from django.db import connections
from mkridit.models import *
import requests
from requests.auth import HTTPBasicAuth
import logging

# Create a logger for this file
logger = logging.getLogger(__file__)



AUTH = HTTPBasicAuth('superadmin', 'ulan')

class Command(BaseCommand):

    def handle(self,*args,**options):
        logger.info("START BRANCH")
        self.collect_branch()
        logger.info("END BRANCH")
        logger.info("-------")
        logger.info("START SERVICES")
        self.collect_services()
        logger.info("END SERVICES")
        logger.info("START PROFILES")  
        self.collect_profiles()
        logger.info("END PROFILESS")


    def collect_branch(self):
        configs = BranchConfig.objects.all().values('branch__orc_id').distinct("branch__orc_id")
        ids = []
        for i in configs:
            ids.append(i.get('branch__orc_id'))


        Branch.objects.exclude(**{"orc_id__in":ids}).delete()


        data = requests.get('ip',auth=AUTH).json()   # burda olmuyannari silmey ve teze olannaridi yaratmaq laizmdi     
        data = [{"branch_id":i.get('id'),"name":i.get('name')} for i in data]
        for i in data:
            if not i.get("branch_id") in ids:
                Branch.objects.create(name=i.get('name'),orc_id=i.get('branch_id'))

        self.all_branchs = Branch.objects.all()

    def collect_services(self):
        Service.objects.all().delete()
        for j in self.all_branchs:
            print(j.orc_id,"BRANCH IDS  IN SERVICES")
            data = requests.get(f'ip/{j.orc_id}/services/',auth=AUTH)
            if not data:
                continue
            data=data.json()
            data = [{"service_id":i.get('id'),"internal_name":i.get('internalName'),"external_name":i.get('externalName')} for i in data]
            for i in data:
                Service.objects.create(name=i.get('internal_name'),orc_id=i.get('service_id'),branch=j)

    def collect_profiles(self):
        Profiles.objects.all().delete()
        for j in self.all_branchs:
            print(j.orc_id,"BRANCH IDS  IN PROFILES")
            data = requests.get(f"ip/{j.orc_id}/profiles",auth=AUTH)
            
            if not data:
                continue
            data = data.json()
            for i in data:
                # print(i)
                Profiles.objects.create(name=i.get('name'),orc_id=i.get('id'),branch=j)

