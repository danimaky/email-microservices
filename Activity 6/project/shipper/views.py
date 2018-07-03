from celery import chain
# Create your views here.
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import FileUploadForm
from .tasks import loadfileactiveusers, sendfile, cleanfolder


class FileView(CreateView):
    form_class = FileUploadForm
    template_name = 'shipper/file_form.html'
    success_url = reverse_lazy('shipper:fileupload')


class GenerateMail(TemplateView):
    template_name = 'shipper/generatemail.html'

    def get(self, request, *args, **kwargs):
        print("entra")
        chain(loadfileactiveusers.s(), sendfile.s(), cleanfolder.s())()
        return render(request, 'shipper/generatemail.html')
