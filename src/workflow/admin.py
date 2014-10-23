from django.contrib import admin
from genericadmin.admin import GenericAdminModelAdmin
from workflow.models import Workflow, Status

class StatusInline(admin.StackedInline):
    model = Status
    extra = 1

class WorkflowAdmin(GenericAdminModelAdmin):
    model = Workflow
    inlines = (StatusInline,)

admin.site.register(Workflow, WorkflowAdmin)
admin.site.register(Status)