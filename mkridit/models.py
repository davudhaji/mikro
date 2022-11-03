from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from datetime import datetime
# Create your models here.


class Branch(models.Model):
    orc_id = models.IntegerField()
    name = models.CharField(max_length=100)

class Service(models.Model):
    branch = models.ForeignKey("Branch",on_delete=models.CASCADE)
    orc_id = models.IntegerField()
    name = models.CharField(max_length=100)

class Profiles(models.Model):
    branch = models.ForeignKey("Branch",on_delete=models.CASCADE)
    orc_id = models.IntegerField()
    name = models.CharField(max_length=100)


class BranchConfig(models.Model):
    branch = models.ForeignKey("Branch",on_delete=models.CASCADE)
    profile_ids = ArrayField(models.IntegerField(),blank=True,null=True)
    service_id = models.IntegerField()



class Report(models.Model):
    phone_number = models.CharField(max_length=20)
    service_id = models.IntegerField()
    service_name = models.CharField(max_length=100)
    branch_id = models.IntegerField()
    branch_name = models.CharField(max_length=100)
    created_at =models.DateTimeField(auto_now_add=True,verbose_name=("Created date"))



class SMTP(models.Model):
    server = models.CharField(max_length=50)
    port = models.IntegerField()
    mail= models.CharField(max_length=60)
    password = models.CharField(max_length=70)
    subject = models.CharField(max_length=150)
    signature = models.TextField()
    to = ArrayField(models.CharField(max_length=70),blank=True,null=True)



    