CELERY_RESULT_BACKEND = 'redis://:redisAdmin@localhost:6379/0'
BROKER_URL = 'redis://:redisAdmin@localhost:6379/0'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_ENABLE_UTC = True
