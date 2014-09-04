# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, Http404

from tracker.models import Ticket


def index(request):
    latest_tickets = Ticket.objects.order_by('-dt_created')[:5]
    output = '<br>'.join([u"{0}: {1}".format(p.id, p.text) for p in latest_tickets])
    return HttpResponse(output)


def ticket(request, ticket_id):
    try:
        poll = Ticket.objects.get(pk=ticket_id)
    except Ticket.DoesNotExist:
        raise Http404
    return HttpResponse(u"<p>{0}: {1}".format(poll.id, poll.text))
    #return render(request, 'polls/detail.html', {'poll': poll})
