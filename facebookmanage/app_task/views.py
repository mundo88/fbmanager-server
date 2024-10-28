from app_task.serializers import AppTaskSerializer,AppTask
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework import filters as res_fillters
from rest_framework import permissions

class AppTaskViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny,]
    serializer_class = AppTaskSerializer
    queryset = AppTask.objects.all()
    filter_backends = (filters.DjangoFilterBackend, res_fillters.SearchFilter)
    filterset_fields = '__all__'
    search_fields = ['title',]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return AppTask.objects.filter(user=user).order_by('-created_at')
        return AppTask.objects.none()