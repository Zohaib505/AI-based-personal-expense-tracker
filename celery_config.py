# Redis/Celery Fix - Add this to settings.py or create a separate config

# Fallback configuration if Redis is not available
import os

# Check if Redis is available, if not disable Celery
try:
    import redis
    redis_client = redis.Redis(host='localhost', port=6379, db=0, socket_connect_timeout=5)
    redis_client.ping()
    CELERY_ENABLED = True
except Exception as e:
    print(f"Warning: Redis not available ({e}). Disabling Celery tasks.")
    CELERY_ENABLED = False
    # Fallback to in-process task execution
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True

# Celery Configuration with timeout handling
if CELERY_ENABLED:
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'UTC'
    CELERY_TASK_TRACK_STARTED = True
    CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
    CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60  # 25 minutes
    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
    CELERY_BROKER_CONNECTION_RETRY = True
    CELERY_BROKER_POOL_LIMIT = 0  # Unlimited pool
    CELERY_BROKER_HEARTBEAT = 30
else:
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True

print(f"Celery enabled: {CELERY_ENABLED}")
