from pickletools import read_unicodestring1
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from .serializer import *
from rest_framework.settings import api_settings
from rest_framework import status
from rest_framework.response import Response



class ReportViewSet(ModelViewSet):
    model = Report
    serializer_class = ReportSerializer
    queryset = Report.objects.all().order_by('-created_at')
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    filter_backends = [filters.SearchFilter]
    # search_fields = ['name']
    http_method_names = ['get']


    def tz_diff(self, date, tz1, tz2):
        import pandas as pd

        date = pd.to_datetime(date)

        return (tz1.localize(date) -
                tz2.localize(date).astimezone(tz1)) \
                   .seconds / 3600



    def list(self, request, **kwargs):
        
        branch, date, service, phone, time,type =  self.request.query_params.getlist('branch[]', None), \
        self.request.query_params.getlist('date[]', None), \
        self.request.query_params.getlist('service[]', None), self.request.query_params.get('phone', None), \
        self.request.query_params.getlist('time', None), self.request.query_params.get('type', None)
        filter_data = {}
        q_list = []

        from django.db.models import Q
        from functools import reduce
        import operator

        if phone:
            filter_data.update({'phone_number__icontains':phone})
        if branch:
            filter_data.update({"branch_id__in": branch})
        if service:
            filter_data.update({"service_id__in": service})            
        if date or time:
            from datetime import timedelta
            import pytz
            from pytz import timezone

            #Bu userin companysinden timezonu tapip saatdan cixib filtirlemeliyem
    
            time_zone = pytz.timezone("Asia/Baku") 
            utc = timezone('UTC')
            diff_hours = self.tz_diff(date[1],utc,time_zone)
            diff_hours = int(str(diff_hours).split('.')[0])

            date[1] = date[1] + " " + str(timedelta(hours=23-diff_hours, minutes=23, seconds=23))
        
            filter_data.update({"created_at__range": date})
        
    
        if filter_data:
            data = Report.objects.filter(**filter_data)
            print(data,'dataa')
            if not type:
                page = self.paginate_queryset(data)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)
            elif type=='all':
                serial = self.get_serializer(data, many=True)
                print(serial)
                return Response(serial.data)
            
        else:
            if type=='all':
                all_data=Report.objects.all()
                serial = self.get_serializer(all_data, many=True)
                return Response(serial.data)
            return super().list(request,**kwargs)
            