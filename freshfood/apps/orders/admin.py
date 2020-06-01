from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'phone_number', 'email',
                    'address', 'paid', 'braintree_id', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated',
                   'first_name', 'last_name', 'phone_number']
    inlines = [OrderItemInline]
