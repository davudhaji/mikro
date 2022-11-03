from rest_framework import serializers
from mkridit.models import *
from rest_framework.exceptions import ValidationError


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('__all__')

    
    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     service= Service.objects.filter(orc_id=instance.service_id,branch__branch_id=instance.branch_id).last()
    #     branch = Branch.objects.filter(branch_id=instance.branch_id).last()
    #     print(instance.service_id,'thisss service iddd',service)
    #     data.update({"service_name":service.name,"branch_name":branch.name})
    #     return data