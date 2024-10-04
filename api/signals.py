from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
import threading



@receiver(post_save, sender=Order)
def update_total_price(sender, instance, created, **kwargs):
    if created:
        job = instance.job
        if job:
            total_price = sum(order.price for order in Order.objects.filter(job=job))
            job.total_price = total_price
            job.save()

@receiver(post_save, sender=Order)
def update_pending_orders_count(sender, instance, **kwargs):
    job = instance.job
    if job:
        job.pending_order = Order.objects.filter(job=job, status='PD').count()
        job.save()

def update_total_price_async(job_id):
    threading.Thread(target=update_total_price, args=(job_id,)).start()