from django.conf import settings
from django.urls import path, include
from . import views
from rest_framework import routers


if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.register(r'siteinfo', views.SiteInfoViewset)

urlpatterns = [
    path('', include(router.urls)),
]