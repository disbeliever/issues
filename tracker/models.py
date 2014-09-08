# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class TicketStatus(models.Model):
    status = models.CharField(max_length=100)

    def __unicode__(self):
        return self.status


class Ticket(models.Model):
    project = models.ForeignKey(Project)
    text = models.CharField(max_length=1500)
    status = models.ForeignKey(TicketStatus)
    author = models.ForeignKey(User, related_name='author')
    assigned_user = models.ForeignKey(User, blank=True, null=True)
    dt_created = models.DateTimeField('date/time created')

    def __unicode__(self):
        return "{0}:".format(self.id, self.text[0:100])


class TicketHistory(models.Model):
    ticket = models.ForeignKey(Ticket)
    dt = models.DateTimeField('date/time')
    text = models.CharField(max_length=1500)
    user = models.ForeignKey(User)
    status = models.ForeignKey(TicketStatus)

    def __unicode__(self):
        return "Ticket {0} {1}: {2}".format(ticket.id, dt, text)
