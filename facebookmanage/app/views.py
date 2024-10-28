from rest_framework.response import Response
from app.serializers import AppSerializer,App,AppTag,TagSerializer,AppCategory,CategorySerializer,AppComment,CommentSerializer,AppChangelog,ChangelogSerializer
from rest_framework import viewsets,views,permissions,filters,status
from rest_framework.decorators import action
from django.conf import settings
import os
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

class AppPagination(PageNumberPagination):
    page_size = 15  # You can adjust this value as needed

class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'category__name', 'author__username', 'tags__name']
    filterset_fields = ['category', 'tags']
    pagination_class = AppPagination
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        app = self.get_object()
        comments = AppComment.objects.filter(app=app).order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_comment(self, request, pk=None):
        app = self.get_object()  # Lấy ứng dụng hiện tại
        # Sao chép dữ liệu từ request
        data = request.data.copy()
        data['app'] = app.id  # Gán ứng dụng vào bình luận
        serializer = CommentSerializer(data=data, context={'request': request})  # Chuyển context để sử dụng trong serializer
        if serializer.is_valid():
            serializer.save()  # Lưu bình luận vào DB
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def changelogs(self, request, pk=None):
        app = self.get_object()
        changelogs = AppChangelog.objects.filter(app=app)
        serializer = ChangelogSerializer(changelogs, many=True)
        return Response(serializer.data)
    
    
class TagViewSet(viewsets.ModelViewSet):
    queryset = AppTag.objects.all()
    serializer_class = TagSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = AppCategory.objects.all()
    serializer_class = CategorySerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = AppComment.objects.all()
    serializer_class = CommentSerializer

class ChangelogViewSet(viewsets.ModelViewSet):
    queryset = AppChangelog.objects.all()
    serializer_class = ChangelogSerializer


class InstallAppViewSet(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        installed_apps = request.user.installed_apps
        app_id = request.data.get('appId')
        app = App.objects.get(id=app_id)
        file_path = os.path.join(settings.MEDIA_ROOT, app.main_file.name)
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=app.main_file.name)
            app_id = request.data.get('appId')
            request.user.installed_apps.add(app)
            app.download_count += 1
            app.save()
            return response
        else:
            return Response({"error": "File không tồn tại"}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request):
        app_id = request.data.get('appId')
        app = App.objects.get(id=app_id)
        request.user.installed_apps.remove(app)
        return Response({'message': 'App uninstalled successfully.'})
    