# myapp/urls.py
from django.urls import include, path
from . import views
from rest_framework import routers


routes = routers.DefaultRouter()
routes.register(r'', views.AppTaskViewSet, basename='app_task')
urlpatterns = [
    path('', include(routes.urls)),
]
