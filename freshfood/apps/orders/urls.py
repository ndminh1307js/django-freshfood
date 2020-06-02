from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('admin/order/<int:order_id>/',
         views.OrderAdminDetailView.as_view(), name='admin_order_detail'),
]
