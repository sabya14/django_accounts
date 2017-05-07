from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^files/', include('files.urls',namespace='files')),
    url(r'^profiles/', include('profiles.urls', namespace='profiles')),

]
