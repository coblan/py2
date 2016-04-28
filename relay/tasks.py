BROKER_URL = 'redis://localhost:6379/0'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

from celery import Celery

app = Celery('tasks', backend=BROKER_URL, broker=BROKER_URL)
#app.conf.CELERY_IGNORE_RESULT=False
app.conf.CELERY_RESULT_BACKEND="redis"

@app.task
def add(x, y):
    return x + y