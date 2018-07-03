from django import forms
from django.db.transaction import commit

from .models import File
from .tasks import analize, massiveregisterusers


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['upload']

        labels = {
            'upload': 'File to upload',
        }
        widgets = {
            'upload': forms.FileInput()
        }

    def save(self, commit=True):
        file = super(FileUploadForm, self).save(commit=commit)
        massiveregisterusers.delay(file.id)
        return file
