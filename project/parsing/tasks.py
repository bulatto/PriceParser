from celery import shared_task

from parsing.helpers import run_price_task


@shared_task
def run_celery_price_task(product_id):
    run_price_task(product_id)
