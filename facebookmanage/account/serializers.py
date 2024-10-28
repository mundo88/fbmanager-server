from rest_framework import serializers
from account.models import Account,AccountSettings
from drf_queryfields import QueryFieldsMixin
from rest_framework_simplejwt import serializers as jwt_serializers
from rest_framework_simplejwt import exceptions as rest_exceptions

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountSettings
        fields = '__all__'
    
# Serializers define the API representation.
class UserSerializer(QueryFieldsMixin,serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    avatar = serializers.ImageField(required=False)
    name = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    settings = SettingSerializer(required=False)
    # Liên kết với AccountSettings
    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'avatar', 'name','settings')
        write_only_fields = ('password',)
        
    def to_representation(self, instance):
        # Gọi phương thức to_representation của lớp cha để lấy dữ liệu ban đầu
        representation = super().to_representation(instance)
        request = self.context.get('request')

        # Thêm full path cho trường avatar nếu nó tồn tại
        if instance.avatar and request:
            representation['avatar'] = request.build_absolute_uri(instance.avatar.url)
        return representation
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
class CookieTokenRefreshSerializer(jwt_serializers.TokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise rest_exceptions.InvalidToken(
                'No valid token found in cookie \'refresh\'')


class ChangePasswordSerializer(serializers.Serializer):
    model = Account
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
    
