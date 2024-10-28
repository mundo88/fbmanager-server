
from rest_framework import status,viewsets,permissions
from facebook_account.serializers import FbAccountSerializer,FacebookAccount,ChromeProfile,ChromeProfileSerializer
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from facebook_account.filters import FbAccountFilterSet
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


class FbAccountViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = FbAccountSerializer
    queryset = FacebookAccount.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = FbAccountFilterSet
    
    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.filter_queryset(self.get_queryset())

        if user.is_authenticated:
            queryset = queryset.filter(collaborators=user)
        queryset = queryset.order_by('-id')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def bulk_update_facebook_accounts(self, request):
        """Update multiple FacebookAccounts in bulk."""
        # Dữ liệu gửi lên từ client phải là một danh sách các tài khoản cần cập nhật
        accounts_data = request.data

        # Kiểm tra nếu dữ liệu gửi lên là danh sách
        if not isinstance(accounts_data, list):
            return Response({"detail": "Invalid data format. A list of accounts is expected."},
                            status=status.HTTP_400_BAD_REQUEST)

        updated_accounts = []  # Danh sách để lưu các tài khoản đã được cập nhật
        errors = []  # Danh sách để lưu các lỗi nếu có
        for account_data in accounts_data:
            account_id = account_data.get('id')
            if not account_id:
                errors.append({"detail": "ID is required for each account."})
                continue
            # Lấy FacebookAccount theo id
            try:
                fb_account = get_object_or_404(FacebookAccount, id=account_id)
            except FacebookAccount.DoesNotExist:
                errors.append({"detail": f"FacebookAccount with id {account_id} not found."})
                continue
            # Sử dụng serializer để cập nhật từng account
            serializer = FbAccountSerializer(fb_account, data=account_data, partial=True)
            if serializer.is_valid():
                serializer.save()  # Lưu tài khoản đã cập nhật
                updated_accounts.append(serializer.data)  # Thêm vào danh sách đã cập nhật
            else:
                errors.append(serializer.errors)  # Lưu lỗi nếu có
        if errors:
            return Response({"updated_accounts": updated_accounts, "errors": errors},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"updated_accounts": updated_accounts}, status=status.HTTP_200_OK)
    #     return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        instance.collaborators.add(request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['get'])
    def chrome_profile(self, request, pk=None):
        """Custom action to retrieve the ChromeProfile for a specific FacebookAccount."""
        try:
            fb_account = self.get_object()  # Get the FacebookAccount instance by pk
        except FacebookAccount.DoesNotExist:
            raise NotFound("Facebook account not found")
        
        try:
            chrome_profile = fb_account.chrome_profile  # Get the associated ChromeProfile
        except ChromeProfile.DoesNotExist:
            raise NotFound("Chrome profile not found for this Facebook account")
        
        serializer = ChromeProfileSerializer(chrome_profile)
        return Response(serializer.data)
    
    @action(detail=True, methods=['put', 'patch'])
    def update_chrome_profile(self, request, pk=None):
        """Update the ChromeProfile for a specific FacebookAccount."""
        try:
            fb_account = self.get_object()
        except FacebookAccount.DoesNotExist:
            raise NotFound("Facebook account not found")

        try:
            chrome_profile = fb_account.chrome_profile  # Lấy profile cần cập nhật
        except ChromeProfile.DoesNotExist:
            raise NotFound("Chrome profile not found for this Facebook account")

        # Cập nhật dữ liệu từ request
        serializer = ChromeProfileSerializer(chrome_profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)