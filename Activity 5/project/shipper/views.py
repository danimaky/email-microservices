from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView

from .forms import FileUploadForm
from .models import File


class FileView(CreateView):
    form_class = FileUploadForm
    template_name = 'shipper/file_form.html'
    success_url = reversed('shipper:')
