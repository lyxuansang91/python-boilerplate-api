from celery import Celery

from app.core.config import settings
from app.jobs.crawl.edinet.edinet_crawler import EdinetCrawler

# Create Celery app
celery = Celery(
    'tasks',
    broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0'
)

# Configure Celery
celery.conf.update(
    timezone='Asia/Ho_Chi_Minh',
    enable_utc=True
)


@celery.task
def monthly_task():
    """Task that runs on 3rd day of every month"""
    try:
        crawler = EdinetCrawler()
        crawler.run()
        print("Running monthly task on 3rd day")

    except Exception as e:
        print(f"Error in monthly task: {str(e)}")
        raise


# Schedule configuration
celery.conf.beat_schedule = {
    'monthly-task-3rd-day': {
        'task': 'app.workers.tasks.monthly_task',
        # 'schedule': crontab(day_of_month='3', hour='0', minute=''),
        'schedule': 30.0,
    },
}
