from django.urls import path, include
from rest_framework import routers


from . import views, login, email_handle, need

router = routers.DefaultRouter()
router.register(r'members', views.ReactMemberViewSet)
router.register(r'needs', views.ReactNeedFullViewSet)
# router.register(r'update-needs', views.ReactNeedUpdateViewSet)
router.register(r'needs-summary', views.ReactNeedSummaryViewSet)
router.register(r'needs-working', views.ReactNeedWorkingViewSet)
router.register(r'need-follow-up', views.ReactFollowUpViewSet)
router.register(r'need-assessment', views.ReactNeedAssessmentViewSet)

urlpatterns = [

    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('members/<int:member_id>/accept/', views.reactMemberConfirmViewSet),
    path('login/', login.user_login),
    path('signup/', login.user_signup),
    path('list-devices/', login.get_devices),
    path('logout/', login.log_out),
    path('remove-device/', login.remove_device),
    path('myinfo/', login.get_authenticated),
    path('member-signup/', login.member_signup),
    path('send-email/', email_handle.send_email),
    path('need/submit', need.need_submit),
    # path('reactmembers/', views.ReactMemberViewSet.as_view())
]