from django.conf.urls import url

from .views import FileView

app_name = 'shipper'


urlpatterns = [
    url(r'^file/upload/$', FileView.as_view(), name='fileupload'),
]