from django.urls import path
from .views import list_order, create_order, update_order

urlpatterns = [
    path('orders', list_order, name="list_order"),
    path('orders/create', create_order, name="create_order"),
    path('orders/<int:id>', update_order, name="update_order"),
]