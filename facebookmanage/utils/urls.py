from django.urls import path
from .views import LanguageListView

urlpatterns = [
    path('api/languages/', LanguageListView.as_view(), name='language-list'),
]
