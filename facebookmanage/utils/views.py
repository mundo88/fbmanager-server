from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LanguageSerializer

class LanguageListView(APIView):
    CHROME_LANGUAGE_CHOICES = [
        ('en-US', 'Tiếng Anh (Hoa Kỳ)'),
        ('en-GB', 'Tiếng Anh (Anh)'),
        ('vi', 'Tiếng Việt'),
        ('fr', 'Tiếng Pháp'),
        ('de', 'Tiếng Đức'),
        ('es', 'Tiếng Tây Ban Nha'),
        ('zh-CN', 'Tiếng Trung (Giản thể)'),
        ('zh-TW', 'Tiếng Trung (Phồn thể)'),
        ('ja', 'Tiếng Nhật'),
        ('ko', 'Tiếng Hàn'),
        ('ru', 'Tiếng Nga'),
        ('pt-BR', 'Tiếng Bồ Đào Nha (Brazil)'),
        ('it', 'Tiếng Ý'),
        ('ar', 'Tiếng Ả Rập'),
        ('th', 'Tiếng Thái'),
        ('id', 'Tiếng Indonesia'),
        ('nl', 'Tiếng Hà Lan'),
        ('el', 'Tiếng Hy Lạp'),
        ('pl', 'Tiếng Ba Lan'),
    ]

    def get(self, request):
        languages = [
            {"code": code, "name": name}
            for code, name in self.CHROME_LANGUAGE_CHOICES
        ]
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
