from django.urls import path, include
from rest_framework import routers


from . import views, login

router = routers.DefaultRouter()
router.register(r'reactmembers', views.ReactMemberViewSet)

urlpatterns = [

    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('reactmembers/<int:member_id>/accept/', views.reactMemberConfirmViewSet),
    path('reactlogin/', login.user_login),
    # path('reactmembers/', views.ReactMemberViewSet.as_view())
]