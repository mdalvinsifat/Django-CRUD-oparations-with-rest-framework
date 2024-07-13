from rest_framework import serializers
from . import models

class ServiceSerializers(serializers.ModelSerializer):
    class Meta : 
        model = models.ServiceModels
        fields = '__all__'
        