from django.conf.urls import url

from .views import FileView, GenerateMail

app_name = 'shipper'


urlpatterns = [
    url(r'^file/upload/$', FileView.as_view(), name='fileupload'),
    url(r'^file/download/$', GenerateMail.as_view(), name='filedownload'),
]