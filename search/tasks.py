# -*- coding: utf-8 -*-
from django.core.management import call_command
from celery.decorators import periodic_task
from celery.task.schedules import crontab


@periodic_task(run_every=crontab(hour='0', minute='0'))
def periodic_rebuild_index():

    call_command('rebuild_index', interactive=False, verbosity=0)
