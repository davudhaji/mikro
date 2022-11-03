from http import server
import profile
from venv import create
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from rest_framework import status
from requests.auth import HTTPBasicAuth
from django.shortcuts import get_object_or_404
# import psycopg2
import json
import psycopg2
from mkridit.models import *
from rest_framework.exceptions import ValidationError
import pandas as pd
import os
from datetime import datetime, timedelta
from pytz import timezone              
import logging
logger = logging.getLogger(__name__)


AUTH = HTTPBasicAuth('superadmin', 'ulan')



class ExportAPI(APIView):
    def post(self,request):
        # column_name = ['x','y','z','n']
        type = request.query_params.get('type', None)
        data = json.loads(request.body)
        url,file = self.export(data,type)        

        return Response(url,200)


    @staticmethod
    def export(data,type='pdf'):
        time,numbers,services_id,service_name,branchs_id,branchs_name,created_at=[],[],[],[],[],[],[]
        full_data = {"Date":created_at, "Time":time,"Branch name":branchs_name,"Service name":service_name,"Phone":numbers, "":""}
        for i in data:
            # ids.append(i.get('id'))
            numbers.append(i.get('phone_number'))
            services_id.append(i.get('service_id'))
            service_name.append(i.get('service_name'))
            branchs_id.append(i.get('branch_id'))
            branchs_name.append(i.get('branch_name'))
            created_at.append(i.get('created_at').split('T')[0])
            time.append(i.get('created_at').split('T')[1].split('.')[0])
        # print(full_data,"full")
        df = pd.DataFrame(full_data)
        url,file = ExportAPI.get_file_url(df=df,file_type=type)

        return url,file
    
    @staticmethod
    def get_file_url(df, file_type):
        import pdfkit
        print(file_type,'tyeee')
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        if not os.path.exists('media'):
            os.makedirs('media')
        url = ''
        if not isinstance(df, pd.DataFrame):
            df = df.to_frame()
        try:
            df = df.drop(df.columns[-1], axis=1)
        except:
            pass
        if file_type == 'xlsx':
            url = f"media/output-{now}.xlsx"
            df.to_excel(url,index=False)
        if file_type == 'csv':
            url = f"media/output-{now}.csv"
            df.to_csv(url, encoding='utf-8',index=False)
        elif file_type == 'pdf':
            url = f"media/output-{now}.pdf"
            html = f"media/output-{now}.html"
            f = open(html, 'w')
            html_data = df.to_html(index=False)
            f.write('<meta charset="UTF-8">')
            f.write(html_data)
            f.close()
            pdfkit.from_file(html, url)
        return os.path.join("http:///", url),url




class ServisAPI(APIView):
    def post(self,request):
        data = json.loads(request.body)
        if not data:
            return Response('Service id not valid',400)

        service_id = data.get('service_id')
        branch_id = data.get('branch_id')
        ip = data.get('ip')
        print(branch_id,service_id,'all dataa')




        profiles = BranchConfig.objects.filter(branch__orc_id=branch_id,service_id=service_id).values('profile_ids')
        if profiles:
            profiles = tuple(list(profiles)[0].get('profile_ids'))
            print(profiles,'proofileeess')
        else:
            return Response({'online':False})


        if len(profiles)==1:
            prof_id = profiles[0]
            profiles = '('+str(prof_id)+')'
            


        conn = psycopg2.connect(
        database="", user='', password='', host=f'{ip}', port= '5432'
        )
        cursor = conn.cursor()
        
        query = f"""
        select id from cfm_work_profile where orig_id in {profiles};
        """
        cursor.execute(query)
        dbdata = cursor.fetchall()
        profiles = set(dbdata)
        print(profiles,'profiless')
        new_profiles = []
        for i in profiles:
            new_profiles.append(i[0])
        print(new_profiles,'THISS NEWW PROF')




        data = requests.get(f'ip/{branch_id}/servicePoints/',auth=AUTH)
        if not data:
            return Response('Not service points',400)

        data = data.json()

        print(data,'THIS DATAA')

        for i in data:
       
            if i.get('workProfileId') in new_profiles:
                return Response({'online':True},200)
            print(i.get('workProfileId'),"iii")


        return Response({'online':False},200)


class BranchsAPI(APIView):
    def get(self,request):
        branch_search = request.query_params.get('branch', None)
        data = Branch.objects.all().order_by("name").values("orc_id","name")
        # data.raise_for_status() 
        
        data = [{"branch_id":i.get('orc_id'),"name":i.get('name')} for i in data] 
        # for i in data:
        #     Branch.objects.create(name=i.get('name'),branch_id=i.get('branch_id'))
        if branch_search:
            new_list = []
            for i in data:
                if branch_search.upper() in i.get('name').upper():
                    new_list.append(i)

            return Response(new_list)
            
        
        return Response(data=data,status=200)


class ReportBranchs(APIView):
    def get(self,request):
        
        all_d = Report.objects.all().extra(
        select={
            'name': 'branch_name',
            'id' : 'branch_id'    
        }
        ).values(
        'name',
        'id'
        ).distinct('branch_id')

        return Response(data=all_d)

class AllServicesAPI(APIView):
    def get(self,request):
        

        all_d = Report.objects.all().extra(
        select={
            'name': 'service_name',
            'id' : 'service_id'    
        }
        ).values(
        'name',
        'id'
        ).distinct('service_id')

        return Response(data=all_d)




class ServicesAPI(APIView):
    def get(self,request,pk):
        from django.db.models import F 
        data = Service.objects.filter(branch__orc_id=pk).order_by("name").values("orc_id","name")
        service_search = request.query_params.get('service', None)
        if not data:
            data = []
            return Response(data)
       
        data = [{"service_id":i.get('orc_id'),"external_name":i.get('name')} for i in data]
        
        if service_search:
            new_list = []
            for i in data:
                if service_search.upper() in i.get('external_name').upper():
                    new_list.append(i)

            return Response(new_list)
        return Response(data)

class ProfilesAPI(APIView):
    def get(self,request,pk):
        data = Profiles.objects.filter(branch__orc_id=pk).order_by("name").values('name','orc_id')
        data = [{"id":i.get('orc_id'),"name":i.get('name')} for i in data]
        if not data:
            data = []
            return Response(data)
        return Response(data)



class ConfigAPI(APIView):
    def post(self,request,pk):
        all_data = json.loads(request.body)
        
        if not all_data:
            return Response('Json not valid',400)


        # BURDA FERQLI SERVICESERE  EYNI PROFILE IDNIN DUESMEYI DUZ DEYIL BUNU CHEK ELE DUZELT
        for data in all_data:    
            service_id = data.get('service_id')
            profiles_ids = data.get('profiles')

            
            if BranchConfig.objects.filter(service_id=service_id,branch__orc_id=pk).last():
                BranchConfig.objects.filter(service_id=service_id,branch__orc_id=pk).update(profile_ids=profiles_ids)
            
            else:
                if not Branch.objects.filter(orc_id=pk):
                    Branch.objects.create(orc_id=pk)
                branch = Branch.objects.get(orc_id=pk)
                BranchConfig.objects.create(service_id=service_id,profile_ids=profiles_ids,branch=branch)
            data = BranchConfig.objects.filter(branch__orc_id=pk,service_id=service_id).values('service_id','profile_ids')

        return Response(all_data,200)

    def get(self,request,pk):
        data = BranchConfig.objects.filter(branch__orc_id=pk).values('service_id','profile_ids')
        return Response(data=data,status=200)



class ReportAPI(APIView):
    def get(self,request):
        all_data = Report.objects.all().values('created_at','branch','service_id','phone_number')

        return Response(all_data,200)

    
class NumberAPI(APIView):
    def post(self,request):
        all_data = json.loads(request.body)
        service_id = all_data.get('service_id')
        branch_id = all_data.get('branch_id')
        phone_number = all_data.get('number')

        br = Branch.objects.filter(orc_id=branch_id).last()
        sr = Service.objects.filter(orc_id=service_id).last()
        data = Report.objects.create(service_id=service_id,phone_number=phone_number,branch_id=branch_id,branch_name=br.name,service_name=sr.name)
        

        return Response("Success",200)




class SMTPAPI(APIView):
    def get(self,request):
        data = SMTP.objects.all()
        if not data:
            return Response([],200)
        data = data.values('server','port','mail','password','subject','signature','to')

        return Response(data,200)


    def post(self,request):
        all_data = json.loads(request.body)
        server = all_data.get('server')
        port = all_data.get('port')
        mail = all_data.get('mail')
        password = all_data.get('password')
        subject = all_data.get('subject')
        signature = all_data.get('signature')
        to = all_data.get('to')
        


        if SMTP.objects.all():
            obj = SMTP.objects.last()
            SMTP.objects.filter(id=obj.id).update(server=server,port=port,mail=mail,password=password,subject=subject,signature=signature,to=to)
        
        else:
            SMTP.objects.create(server=server,port=port,mail=mail,password=password,subject=subject,signature=signature,to=to)


        return Response(all_data,200)