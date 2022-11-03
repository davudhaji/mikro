from rest_framework import routers
from django.urls import path,include
from django.contrib import admin

from ..models import Report
from .views import SMTPAPI, AllServicesAPI, NumberAPI, ProfilesAPI, ReportAPI, ServicesAPI, ServisAPI,BranchsAPI,ConfigAPI,ExportAPI,ReportBranchs
from .viewset import ReportViewSet


router = routers.SimpleRouter()
router.register(r'report',  ReportViewSet, basename='report')


urlpatterns = [
    path('ticket/', ServisAPI.as_view()),
    path('branches/', BranchsAPI.as_view()),
    path('services/<int:pk>/', ServicesAPI.as_view()),
    path('profiles/<int:pk>/', ProfilesAPI.as_view()),
    path('config/<int:pk>/',ConfigAPI.as_view()),
    path('number/',NumberAPI.as_view()),
    # path('report/',ReportAPI.as_view()),
    path('smtp/',SMTPAPI.as_view()),
    path('export/',ExportAPI.as_view()),
    path('allservices/',AllServicesAPI.as_view()),
    path('allbranches/',ReportBranchs.as_view()),
    path('', include(router.urls))


]