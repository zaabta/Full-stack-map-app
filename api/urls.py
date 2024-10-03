from django.urls import path
from .views import list_order, create_order, update_order, create_job, sort_orders

urlpatterns = [
    path('orders', list_order, name="list_order"),
    path('orders/create', create_order, name="create_order"),
    path('orders/<int:id>', update_order, name="get_or_update_order"),
    path('orders/sort', sort_orders, name="sort_orders"),
    path('job/create', create_job, name="create_job"),
]