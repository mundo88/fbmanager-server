
# Create your views here.
from account.models import Account,AccountSettings
from rest_framework import viewsets,permissions
from account.serializers import (
    UserSerializer,UserLoginSerializer,
    CookieTokenRefreshSerializer,
    SettingSerializer,
    ChangePasswordSerializer
)
from app.serializers import AppSerializer 
from rest_framework import status,generics
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework_simplejwt import tokens,exceptions as rest_exceptions,views as jwt_views
from django.conf import settings
from django.contrib.auth import authenticate
from django.middleware import csrf


def get_user_tokens(user):
    refresh = tokens.RefreshToken.for_user(user)
    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token)
    }


class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Account.objects.all()
    serializer_class = UserSerializer

class UserAppsViewSet(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        installed_apps = request.user.installed_apps
        serializer = AppSerializer(installed_apps, many=True)
        return Response(serializer.data)
    
class CurrentUserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)
    
class UserLoginViewSet(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()   
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user:
                tokens = get_user_tokens(user)
                res = Response()
                res.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value=tokens["access_token"],
                    expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                res.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                    value=tokens["refresh_token"],
                    expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                res.data = tokens
                res["X-CSRFToken"] = csrf.get_token(request)
                return res
            raise rest_exceptions.AuthenticationFailed(
                "Email or Password is incorrect!",400)
        return Response({
            'error_messages': serializer.errors,
            'error_code': 400,
            'success':0
        }, status=status.HTTP_400_BAD_REQUEST)


class CookieTokenRefreshView(jwt_views.TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                value=response.data['refresh'],
                expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )

            del response.data["refresh"]
        response["X-CSRFToken"] = request.COOKIES.get("csrftoken")
        return super().finalize_response(request, response, *args, **kwargs)     
    
class LogoutViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None):
        try:
            refreshToken = request.COOKIES.get(
                settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
            token = tokens.RefreshToken(refreshToken)
            token.blacklist()
            res = Response()
            res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
            res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
            res.delete_cookie("X-CSRFToken")
            res.delete_cookie("csrftoken")
            res["X-CSRFToken"]=None
            return res
        except Exception as e:
            print(e)
            raise rest_exceptions.InvalidToken("Invalid token")
        
class ChangePasswordView(generics.UpdateAPIView):
        serializer_class = ChangePasswordSerializer
        model = Account
        permission_classes = (permissions.IsAuthenticated,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("current_password")):
                    return Response({"current_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }
                return Response(response)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class SettingViewSet(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SettingSerializer
    def get_queryset(self):

        # Trả về chỉ cài đặt của người dùng hiện tại
        return AccountSettings.objects.filter(user=self.request.user)
    def get_object(self):
        print("User settings:", self.request.user.settings)
        # Trả về cài đặt của người dùng hiện tại (OneToOneField)
        return self.request.user.settings
    def perform_update(self, serializer):
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            print("Settings updated successfully")
        else:
            print("Validation errors:", serializer.errors)  # In ra lỗi nếu có
    def update(self, request, *args, **kwargs):
        print("Request data:", request.data)  # In ra dữ liệu từ request
        return super().update(request, *args, **kwargs)