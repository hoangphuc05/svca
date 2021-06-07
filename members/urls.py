from django.urls import path, include
from rest_framework import routers


from . import views, login

router = routers.DefaultRouter()
router.register(r'members', views.ReactMemberViewSet)
router.register(r'needs', views.ReactNeedViewSet)

urlpatterns = [

    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('members/<int:member_id>/accept/', views.reactMemberConfirmViewSet),
    path('login/', login.user_login),
    path('signup/', login.user_signup),
    path('list-devices/', login.get_devices),
    path('logout/', login.log_out),
    path('remove-device/', login.remove_device),
    # path('reactmembers/', views.ReactMemberViewSet.as_view())
]