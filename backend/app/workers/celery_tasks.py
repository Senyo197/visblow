from core.celery import celery_app

# Auto-discover tasks inside modules
celery_app.autodiscover_tasks(["app.modules"])
