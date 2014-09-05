# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader

from tracker.models import Ticket


def index(request):
    latest_tickets = Ticket.objects.order_by('-dt_created')[:5]
    template = loader.get_template('tracker/index.html')
    context = RequestContext(request, {
        'latest_tickets': latest_tickets,
    })
    return HttpResponse(template.render(context))


def ticket(request, ticket_id):
    try:
        ticket = Ticket.objects.get(pk=ticket_id)
    except Ticket.DoesNotExist:
        raise Http404
    return HttpResponse(u"<p>{0}: {1}".format(ticket.id, ticket.text))
