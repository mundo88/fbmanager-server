# myapp/urls.py
from django.urls import include, path
from . import views
from rest_framework import routers



router = routers.DefaultRouter()
router.register(r'', views.AppViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('tags', views.TagViewSet.as_view({'get':'list'}), name='tags'),
    path('categories', views.CategoryViewSet.as_view({'get':'list'}), name='categories'),
    path('install', views.InstallAppViewSet.as_view(), name='install-app'),
]