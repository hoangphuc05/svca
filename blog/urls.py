from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'post-content', views.PostContentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]