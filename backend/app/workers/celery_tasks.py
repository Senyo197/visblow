from backend.app.core.celery_app import celery_app

# Auto-discover tasks inside modules
celery_app.autodiscover_tasks(["app.modules"])
