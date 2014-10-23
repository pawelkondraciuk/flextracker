# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

admin.site.register(Permission)
admin.site.register(ContentType)