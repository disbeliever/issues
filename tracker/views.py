# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from tracker.models import Ticket, TicketStatus, TicketHistory, Project

from email.mime.text import MIMEText
import smtplib
from tracker.settings import EMAIL_FROM, EMAIL_USER, EMAIL_SERVER, EMAIL_PORT, EMAIL_PASSWORD, EMAIL_SSL


def login(request):
    return render(request, 'tracker/login.html', {
        'next': request.GET['next']
        })


@login_required
def index(request):
    if ('ticket_status_id' not in request.POST or
        request.POST['ticket_status_id'] == ''):
        latest_tickets = Ticket.objects
        filter_status_id = None
    else:
        latest_tickets = Ticket.objects.filter(status__id=request.POST['ticket_status_id'])
        filter_status_id = int(request.POST['ticket_status_id'])

    if ('project_id' not in request.POST or
        request.POST['project_id'] == ''):
        filter_project_id = None
    else:
        filter_project_id = int(request.POST['project_id'])
        latest_tickets = latest_tickets.filter(project__id=request.POST['project_id'])

    latest_tickets = latest_tickets.order_by('-dt_created')[:10]


    statuses = TicketStatus.objects.all()
    projects = Project.objects.all()
    context = RequestContext(request, {
        'title': 'Latest tickets',
        'latest_tickets': latest_tickets,
        'statuses': statuses,
        'projects': projects,
        'filter_status_id': filter_status_id,
        'filter_project_id': filter_project_id
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
    if (request.user.is_authenticated()):
        user_id = request.user.id
    else:
        user_id = 0
    t = Ticket(project_id=request.POST['ticket_project'],
               status_id=1,
               author_id=user_id,
               dt_created=timezone.now(),
               text=request.POST['ticket_text'])
    t.save()
    return HttpResponseRedirect(reverse('ticket', args=(t.id,)))


@login_required
def ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    history = TicketHistory.objects.filter(ticket_id=ticket.id).order_by('-dt')
    statuses = TicketStatus.objects.all()
    ticket_emails = [x.strip() for x in ticket.emails_cc.split(',')]
    return render(request, 'tracker/ticket.html', {
        'title': 'Ticket ' + ticket_id,
        'ticket': ticket,
        'history': history,
        'statuses': statuses,
        'ticket_emails': ticket_emails
        })


@login_required
def ticket_add_history(request, ticket_id):
    if (request.user.is_authenticated()):
        user_id = request.user.id
    else:
        user_id = 0
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    th = TicketHistory(status_id=request.POST['ticket_status'],
                       user_id=user_id,
                       ticket_id=ticket.id,
                       dt=timezone.now(),
                       text=request.POST['ticket_text'])
    th.save()
    ticket.status_id = request.POST['ticket_status']
    ticket.save()

    if (EMAIL_SERVER != ''):
        if (EMAIL_SSL):
            smtp = smtplib.SMTP_SSL(EMAIL_SERVER, EMAIL_PORT)
        else:
            smtp = smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT)
        if (EMAIL_USER != '' and EMAIL_PASSWORD != ''):
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
        msg = MIMEText(th.text)
        msg['From'] = EMAIL_FROM
        msg['To'] = ticket.author.email
        if (ticket.emails_cc != ''):
            msg['To'] += "," + ticket.emails_cc
        msg['Subject'] = "Issue tracker: ticket {0} - new comment".format(ticket.id)
        smtp.sendmail(EMAIL_FROM,
                      [x for x in ticket.emails_cc.split(',')] +
                      [ticket.author.email],
                      msg.as_string())

    return HttpResponseRedirect(reverse('ticket', args=(ticket.id,)))


@login_required
def ticket_add_me_to_cc(request, ticket_id):
    user = get_object_or_404(User, pk=request.user.id)
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if (user.email not in ticket.emails_cc):
        ticket.emails_cc += ", " + user.email
        ticket.save()
    return HttpResponseRedirect(reverse('ticket', args=(ticket_id,)))


@login_required
def my(request):
    my_tickets = Ticket.objects.filter(author=request.user)[:10]
    context = RequestContext(request, {
        'title': 'My tickets',
        'latest_tickets': my_tickets,
    })
    return render(request, 'tracker/index.html', context)


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
