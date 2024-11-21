from celery import Celery
from app.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

# Initialize Celery
celery_app = Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
# import app.tasks
celery_app.autodiscover_tasks(['app'], force=True)

# from celery import Celery
# from celery.signals import setup_logging
# import logging

# # Configure logging
# @setup_logging.connect
# def configure_logging(loglevel=None, **kwargs):
#     logging.basicConfig(
#         format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
#         level=logging.INFO
#     )

# # Initialize Celery
# def make_celery(broker_url, backend_url):
#     celery_app = Celery(
#         'tasks',
#         broker=broker_url,
#         backend=backend_url
#     )

#     # Comprehensive configuration
#     celery_app.conf.update(
#         task_track_started=True,
#         task_serializer='json',
#         result_serializer='json',
#         accept_content=['json'],
#         timezone='UTC',
#         enable_utc=True,
#         task_routes={
#             'app.tasks.*': {'queue': 'default'}
#         },
#         task_default_queue='default',
#         task_default_exchange='default',
#         task_default_routing_key='default',
#         worker_log_format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
#         worker_task_log_format='[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s] %(message)s'
#     )

#     # Autodiscover tasks
#     celery_app.autodiscover_tasks(['app'], force=True)

#     return celery_app

# # Import your configuration
# from app.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

# # Create Celery app
# celery_app = make_celery(CELERY_BROKER_URL, CELERY_RESULT_BACKEND)