from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'post-content', views.PostContentViewSet)
router.register(r'image', views.ImageUploadViewset)

urlpatterns = [
    path('', include(router.urls)),
]