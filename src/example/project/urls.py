from django.conf.urls import include, url
from django.contrib.gis import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include("webmap.urls")),
]
