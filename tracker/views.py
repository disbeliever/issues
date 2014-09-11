# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from tracker.models import Ticket, Project


def login(request):
    return render(request, 'tracker/login.html')


@login_required
def index(request):
    latest_tickets = Ticket.objects.order_by('-dt_created')[:10]
    context = RequestContext(request, {
        'title': 'Latest tickets',
        'latest_tickets': latest_tickets,
    })
    return render(request, 'tracker/index.html', context)


@login_required
def new(request):
    projects = Project.objects.all()
    context = RequestContext(request, {
        'title': 'Add new ticket',
        'projects': projects,
    })
    return render(request, 'tracker/new.html', context)


@login_required
def add(request):
    t = Ticket(project_id=request.POST['ticket_project'],
               status_id=1,
               author_id=1,
               dt_created=timezone.now(),
               text=request.POST['ticket_text'])
    t.save()
    return HttpResponseRedirect(reverse('ticket', args=(t.id,)))


@login_required
def ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    return render(request, 'tracker/ticket.html', {'ticket': ticket})


@login_required
def my(request):
    my_tickets = Ticket.objects.filter(author=request.user)[:10]
    context = RequestContext(request, {
        'title': 'My tickets',
        'latest_tickets': my_tickets,
    })
    return render(request, 'tracker/index.html', context)
