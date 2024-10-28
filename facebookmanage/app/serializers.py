from rest_framework import serializers
from app.models import App,AppTag,AppCategory,AppComment,AppChangelog
from account.serializers import UserSerializer
from drf_queryfields import QueryFieldsMixin
from django.db.models import Avg
from rest_framework.filters import OrderingFilter


# # Serializers define the API representation.
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppTag
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AppCategory
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']  # Các trường cho phép sắp xếp
    ordering = ['created_at']  # Sắp xếp mặc định
    class Meta:
        model = AppComment
        fields = '__all__'
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user  # Gán người dùng hiện tại vào bình luận
        
        return super().create(validated_data)
class ChangelogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppChangelog
        fields = '__all__'

# # Serializers define the API representation.
class AppSerializer(QueryFieldsMixin,serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    category = CategorySerializer(many=False, read_only=True)
    author = UserSerializer(many=False, read_only=True)
    installed = serializers.SerializerMethodField('is_installed')
    rating = serializers.SerializerMethodField('get_rating')
    comment_count = serializers.SerializerMethodField('get_comment_count')  # Thêm trường comment_count
    class Meta:
        model = App
        fields = '__all__'
        
    def is_installed(self, obj):
        request = self.context.get('request', None)
        if not request:
            return False
        user = request.user
        if user.is_authenticated:
            return user.installed_apps.filter(id=obj.id).exists()
        return False
    def get_rating(self, obj):
        comments = AppComment.objects.filter(app=obj)
        avg_rating = comments.aggregate(Avg('rating', default=0)).get('rating__avg') or 0
        rounded_avg = round(avg_rating, 2)  # Rounding to 2 decimal places
        return {
            'count': comments.count(),
            'avg': rounded_avg
        }
    def get_comment_count(self, obj):
        comments = AppComment.objects.filter(app=obj)
        return comments.count()