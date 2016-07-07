from django.conf import settings
from django.db import models

from celery.utils.log import get_task_logger
from celery.app.base import Celery
app = Celery()
app.loader.config_from_object(settings)

logger = get_task_logger(__name__)



@app.task(name="twitter.get_mentions")
def get_mentions():
    logger.info("hoge")    
