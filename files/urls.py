from django.conf.urls import url,include
from django.contrib import admin
from files.views import FileCreate,FileRetrieveUpdateDestroy
urlpatterns = [
    url(r'^$', FileCreate.as_view(), name='create'),
    url(r'^(?P<pk>[0-9]+)/$', FileRetrieveUpdateDestroy.as_view(), name='update'),
]
