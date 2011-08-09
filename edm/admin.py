# -*- coding: UTF-8 -*- #
from django.contrib import admin
from FUTFactory.edm.models import Folder, Document, File

admin.site.register(Folder)
admin.site.register(Document)
admin.site.register(File)