from django.core.mail import send_mail

from celery import task

from .models import Order


@task
def order_created(order_id):
    """
    Task to send email notification
    when an order has been succesfully created
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order #{order_id}'
    message = f'Dear {order.first_name}, \nYou have successfully placed an order.\nYour order number is {order_id}'
    mail_sent = send_mail(
        subject, message, 'admin@freshfood.com', [order.email])
    return mail_sent
