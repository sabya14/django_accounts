from django.conf.urls import url,include
from django.contrib import admin
from  .views import ProfileCreateList, ProfileRetrieveUpdateDestroy,ProfilePasswordUpdate,UserLogin
urlpatterns = [
    url(r'register/$', ProfileCreateList.as_view(), name='register'),
    url(r'login/$', UserLogin.as_view(), name='login'),
    url(r'^(?P<pk>[0-9]+)/update/$', ProfileRetrieveUpdateDestroy.as_view(), name='update'),
    url(r'^(?P<pk>[0-9]+)/update/password/$', ProfilePasswordUpdate.as_view(), name='password_change'),
]
