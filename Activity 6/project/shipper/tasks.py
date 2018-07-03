from __future__ import unicode_literals, absolute_import

from celery import chain
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from project import celery_app as app
from project.settings import ADMIN_EMAIL
from .models import File
from os import remove
import xlrd
import xlsxwriter



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


@app.task
def loadfileactiveusers():
    book = xlsxwriter.Workbook('media/report.xls', {'remove_timezone': True, 'default_date_format': 'dd/mm/yy'})
    sheet = book.add_worksheet()
    users = User.objects.filter(is_active=1)
    fields = ("id",
              "last_login",
              "is_superuser",
              "username",
              "first_name",
              "last_name",
              "email",
              "is_staff",
              "is_active",
              "date_joined")
    for field in range(0, len(fields)):
        sheet.write(0, field, fields[field])
    for user in range(0, len(users)):
        for field in range(0, len(fields)):
            sheet.write(user+1, field, users[user].__getattribute__(fields[field]))
    book.close()
    return 'media/report.xls'


@app.task
def sendfile(path):
    e = EmailMessage()
    e.attach_file(path)
    e.body = "Those users are active"
    e.subject = "Users Actives in our server"
    e.to = ADMIN_EMAIL
    e.send()
    return path


@app.task
def cleanfolder(path):
    remove(path)

