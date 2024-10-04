from django.contrib import admin
from django.urls import path
from .views import list_order, create_order, update_order, create_job, sort_orders, get_earned_money, get_pending_orders_count

urlpatterns = [
    path('admin/', admin.site.urls),
    path('order/', list_order, name="list_order"),
    path('order/create', create_order, name="create_order"),
    path('order/<int:id>', update_order, name="get_or_update_order"),
    path('order/sort', sort_orders, name="sort_orders"),
    path('job/create', create_job, name="create_job"),
    path('job/earned-money/<int::id>', get_earned_money, name="get_earned_money"),
    path('job/pending-orders-count/<int::id>', get_pending_orders_count, name="get_pending_orders_count"),
]