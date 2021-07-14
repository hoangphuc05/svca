from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'siteinfo', views.SiteInfoViewset)

urlpatterns = [
    path('', include(router.urls)),
]