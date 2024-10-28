# myapp/urls.py
from django.urls import include, path
from . import views
from rest_framework import routers



router = routers.DefaultRouter()
router.register(r'users', views.UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login', views.UserLoginViewSet.as_view(), name='login'),
    path('refresh-token', views.CookieTokenRefreshView.as_view(),name='refresh'),
    path('me', views.CurrentUserView.as_view(), name='current-user'),
    path('logout', views.LogoutViewSet.as_view(), name='logout'),
    path('installed-apps/', views.UserAppsViewSet.as_view(), name='installed-apps'),
    path('change-password', views.ChangePasswordView.as_view(), name='change-password'),
    path('settings', views.SettingViewSet.as_view(), name='settings'),
]