from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
# Create your views here.


class ContactViewsets (viewsets.ModelViewSet):
    queryset = models.ContactUsModels.objects.all()
    serializer_class = serializers.ContactUsSerializers
    