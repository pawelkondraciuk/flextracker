from django.contrib import admin

# Register your models here.
from projects.models import RoleMembership, Role, Project

admin.site.register(Project)
admin.site.register(Role)
admin.site.register(RoleMembership)