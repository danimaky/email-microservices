from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import User

from project import celery_app as app
from .models import File
import xlrd


# two ways to import app in my other tasks
# from celery import current_app
# app = current_app


@app.task(bind=True)
def prueba(self):
    print("Entro")

@app.task
def analize(file):
    print(File.objects.get(pk=file).upload.name)

@app.task
def massiveregisterusers(file):
    book = xlrd.open_workbook(File.objects.get(pk=file).upload.path)
    users = tuple(book.sheet_by_index(0).get_rows())
    for userrow in range(1, len(users)):
        user = User()
        for data in range(1, len(users[userrow])):
            user.__setattr__(users[0][data].value, users[userrow][data].value)
        print("Users Saved {}".format(userrow))
        user.save()
