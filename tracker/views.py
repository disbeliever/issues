# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader

from tracker.models import Ticket


def index(request):
    latest_tickets = Ticket.objects.order_by('-dt_created')[:5]
    context = RequestContext(request, {
        'title': 'Latest tickets',
        'latest_tickets': latest_tickets,
    })
    return render(request, 'tracker/index.html', context)


def add(request):
    template = loader.get_template('tracker/add.html')
    context = RequestContext(request, {
        'title': 'Add new ticket',
    })
    return render(request, 'tracker/add.html', context)


def ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    return render(request, 'tracker/ticket.html', {'ticket': ticket})
