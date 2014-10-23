from django.contrib import admin

# Register your models here.
from django.contrib.contenttypes.generic import GenericTabularInline, GenericInlineModelAdmin, GenericStackedInline
from projects.forms import UpdateProjectForm
from projects.models import Role, Project
from workflow.models import Workflow


class WorkflowInline(GenericStackedInline):
    model = Workflow
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        WorkflowInline,
    ]

    form = UpdateProjectForm

admin.site.register(Project, ProjectAdmin)
admin.site.register(Role)