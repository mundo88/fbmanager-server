from rest_framework import serializers

class LanguageSerializer(serializers.Serializer):
    code = serializers.CharField()  # Mã ngôn ngữ
    name = serializers.CharField()  # Tên ngôn ngữ
