from django.contrib import admin
from tracker.models import Project,Ticket,TicketStatus

# Register your models here.
admin.site.register(Project)
admin.site.register(Ticket)
admin.site.register(TicketStatus)
