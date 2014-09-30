from django.contrib import admin

# Register your models here.
from projects.models import Role, Project

admin.site.register(Project)
admin.site.register(Role)