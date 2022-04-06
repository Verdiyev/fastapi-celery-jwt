from celery import Celery
from config import settings

from celery.utils.log import get_task_logger



celery = Celery('tasks')
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND

celery_log = get_task_logger(__name__)

#celery -A worker_task worker --pool=eventlet
@celery.task
def get_ip_details(ip):
    from ipdata import ipdata
    ipdata =  ipdata.IPData(settings.IP_API_KEY)
    response = ipdata.lookup(ip)
    return response