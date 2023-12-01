from __future__ import absolute_import, unicode_literals
from celery import Celery;
import os
from kombu import Exchange, Queue
os.environ.setdefault('DJANGO_SETTINGS_MODULE','microservices.settings')
# app = Celery('microservices',backend='celery_amqp_backend.AMQPBackend://')
# app = Celery('tasks', broker='amqp://guest:guest@localhost:5672//',backend='rpc://')
app = Celery('tasks', backend='rpc://', broker='amqp://guest@localhost//')

# app = Celery('documents',backend="celery.backends.amqp:AMQPBackend")
app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks() 