from django.contrib import admin
from issues.models import Ticket

class TicketAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified',)

admin.site.register(Ticket, TicketAdmin)