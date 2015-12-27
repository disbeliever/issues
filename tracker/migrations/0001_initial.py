# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=1500)),
                ('dt_created', models.DateTimeField(verbose_name=b'date/time created')),
                ('emails_cc', models.CharField(max_length=2000)),
                ('assigned_user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('author', models.ForeignKey(related_name='author', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(to='tracker.Project')),
            ],
        ),
        migrations.CreateModel(
            name='TicketHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dt', models.DateTimeField(verbose_name=b'date/time')),
                ('text', models.CharField(max_length=1500)),
            ],
        ),
        migrations.CreateModel(
            name='TicketStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='tickethistory',
            name='status',
            field=models.ForeignKey(to='tracker.TicketStatus'),
        ),
        migrations.AddField(
            model_name='tickethistory',
            name='ticket',
            field=models.ForeignKey(to='tracker.Ticket'),
        ),
        migrations.AddField(
            model_name='tickethistory',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ticket',
            name='status',
            field=models.ForeignKey(to='tracker.TicketStatus'),
        ),
    ]
