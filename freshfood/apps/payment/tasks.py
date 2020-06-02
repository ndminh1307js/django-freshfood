from io import BytesIO
from celery import task
import weasyprint

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from freshfood.apps.orders.models import Order


@task
def payment_completed(order_id):
    """
    Task to send an email notification when an order is successfully created
    """
    order = Order.objects.get(id=order_id)

    # create invoice email
    subject = f'Freshfood - Invoice #{order.id}'
    message = 'Please, find attached the invoice for your recent purchase'
    email = EmailMessage(subject,
                         message,
                         'admin@freshfood.com',
                         [order.email])
    # Generate PDF file
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + '/css/style.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    # attach PDF file
    email.attach(f'order_{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')
    # send email
    email.send()
