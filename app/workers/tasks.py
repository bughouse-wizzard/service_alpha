from app.workers.celery_app import celery_app

@celery_app.task
def example_task(message: str):
    """Example Celery task"""
    return f"Task completed: {message}"