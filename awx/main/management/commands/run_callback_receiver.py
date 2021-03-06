# Copyright (c) 2015 Ansible, Inc.
# All Rights Reserved.

from django.conf import settings
from django.core.management.base import BaseCommand

from awx.main.dispatch.worker import AWXConsumerRedis, CallbackBrokerWorker


class Command(BaseCommand):
    '''
    Save Job Callback receiver
    Runs as a management command and receives job save events.  It then hands
    them off to worker processors (see Worker) which writes them to the database
    '''
    help = 'Launch the job callback receiver'

    def handle(self, *arg, **options):
        consumer = None
        try:
            consumer = AWXConsumerRedis(
                'callback_receiver',
                CallbackBrokerWorker(),
                queues=[getattr(settings, 'CALLBACK_QUEUE', '')],
            )
            consumer.run()
        except KeyboardInterrupt:
            print('Terminating Callback Receiver')
            if consumer:
                consumer.stop()
