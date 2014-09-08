# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils import timezone

from tracker.models import Ticket,Project


def index(request):
    latest_tickets = Ticket.objects.order_by('-dt_created')[:5]
    context = RequestContext(request, {
        'title': 'Latest tickets',
        'latest_tickets': latest_tickets,
    })
    return render(request, 'tracker/index.html', context)


def new(request):
    projects = Project.objects.all()
    context = RequestContext(request, {
        'title': 'Add new ticket',
        'projects': projects,
    })
    return render(request, 'tracker/new.html', context)


def add(request):
    t = Ticket(#project=Project.objects.get(pk=request.POST['ticket_project']),
               project_id=request.POST['ticket_project'],
               status_id=1,
               author_id=1,
               dt_created=timezone.now(),
               text=request.POST['ticket_text'])
    t.save()
    return HttpResponseRedirect(reverse('ticket', args=(t.id,)))


def ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    return render(request, 'tracker/ticket.html', {'ticket': ticket})
