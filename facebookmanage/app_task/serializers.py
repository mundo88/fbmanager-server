from rest_framework import serializers,permissions
from app_task.models import AppTask
from drf_queryfields import QueryFieldsMixin

# Serializers define the API representation.
class AppTaskSerializer(QueryFieldsMixin,serializers.ModelSerializer):

    class Meta:
        model = AppTask
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')  # Lấy request từ context
        user = request.user  # Lấy người dùng đang đăng nhập

        # Tách fb_accounts ra từ validated_data
        fb_accounts_data = validated_data.pop('fb_accounts', [])

        # Tạo đối tượng AppTask với user đã được thiết lập
        app_task = AppTask.objects.create(user=user, **validated_data)

        # Gán fb_accounts cho app_task
        app_task.fb_accounts.set(fb_accounts_data)  # Sử dụng .set() để thiết lập mối quan hệ many-to-many

        return app_task