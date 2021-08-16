from django.urls import path, include
from donation import views
from rest_framework import routers

urlpatterns = [
    # path('ipn_handle/', views.ipn_listener),
    path('list_donation/', views.list_transaction),
]