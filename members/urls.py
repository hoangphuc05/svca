from django.conf import settings
from django.urls import path, include
# from django.conf.urls import url, include
from rest_framework import routers


from . import views, login, email_handle, need, user

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

# router = routers.DefaultRouter()
router.register(r'members', views.ReactMemberViewSet)
router.register(r'needs', views.ReactNeedFullViewSet)
router.register(r'users', views.UserViewSet)
# router.register(r'update-needs', views.ReactNeedUpdateViewSet)
router.register(r'needs-summary', views.ReactNeedSummaryViewSet)
router.register(r'needs-working', views.ReactNeedWorkingViewSet)
router.register(r'need-follow-up', views.ReactFollowUpViewSet)
router.register(r'need-assessment', views.ReactNeedAssessmentViewSet)
# router.register(r'user', user.UserProfileAPIView.as_view())

urlpatterns = [

    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('members/<int:member_id>/accept/', views.reactMemberConfirmViewSet),
    path('login/', login.user_login),
    path('signup/', login.user_signup),
    # path('list-devices/', login.get_devices),
    path('list-devices/', views.GetDevices.as_view()),
    path('logout/', login.log_out),
    path('logout-all/', login.logout_all),
    path('remove-device/', login.remove_device),
    path('myinfo/', login.get_authenticated),
    # path('member-signup/', login.member_signup),
    # path('send-email/', email_handle.send_email),
    path('need/submit', need.need_submit),
    path(r'user/<int:user_id>/', user.UserProfileAPIView.as_view()),
    path('change-password/', views.ChangePasswordView.as_view()),
    # path('sign-up/', views.UserSignup.as_view()),
    path('user-group-update/', views.UserGroupUpdate.as_view()),
    path('check-permission/', login.check_permission),
    path('get-permission/', login.ListPermission.as_view()),
    path('reset-password/', include('django_rest_passwordreset.urls', namespace='password_reset'))

    # path('reactmembers/', views.ReactMemberViewSet.as_view())
]