import watson
from attachments.admin import AttachmentInlines
from django.contrib import admin
from issues.models import Ticket


class TicketAdmin(admin.ModelAdmin):
    inlines = [AttachmentInlines]
    readonly_fields = ('created', 'modified',)


admin.site.register(Ticket, TicketAdmin)