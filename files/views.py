from django.shortcuts import render
from files.serializers import FileSerializer
from rest_framework import generics
from files.models import File
from gridfs import GridFS
from files.utils import create_collection,drop_files
from rest_framework import permissions
# Create your views here.


class FileCreate(generics.ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def perform_create(self, serializer):
        file = self.request.FILES.get('file')
        instance = serializer.save(user=self.request.user)
        instance.file_name = file.name
        instance.save()
        create_collection(instance)



class FileRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_destroy(self, instance):
        queryset = self.get_queryset()
        id = queryset.first().id
        instance = File.objects.get(id=id, user=self.request.user)
        drop_files(instance)
        instance.delete()

    def perform_update(self, serializer):
        queryset = self.get_queryset()
        id = queryset.first().id
        instance = File.objects.get(id=id, user=self.request.user)
        drop_files(instance, 'Update')
        file = self.request.FILES.get('file')
        instance = serializer.save(user=self.request.user)
        instance.file_name = file.name
        instance.save()
        create_collection(instance)
