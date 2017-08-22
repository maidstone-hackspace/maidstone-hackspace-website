from celery import shared_task
from mhackspace.feeds.helper import import_feeds


@shared_task
def update_homepage_feeds():
    return import_feeds()

# @task(bind=True)
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=4, minute=0),
#         update_homepage_feeds.s(),
#     )
