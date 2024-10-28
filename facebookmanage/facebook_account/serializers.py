from rest_framework import serializers
from  facebook_account.models import FacebookAccount,ChromeProfile
from drf_queryfields import QueryFieldsMixin

# # Serializers define the API representation.
class FbAccountSerializer(QueryFieldsMixin,serializers.ModelSerializer):
    chrome_profile = serializers.SerializerMethodField()
    uid = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    class Meta:
        model = FacebookAccount
        fields ='__all__'

    def get_chrome_profile(self, obj):
        chrome_profile = obj.chrome_profile
        if chrome_profile:
            return ChromeProfileSerializer(chrome_profile).data
        return None

class ChromeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChromeProfile
        fields = '__all__'