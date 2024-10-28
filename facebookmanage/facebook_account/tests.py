from django.test import TestCase
from .models import FacebookAccount
import json

class FacebookAccountTestCase(TestCase):
    def setUp(self):
        # Load mock data from JSON file
        with open('./MOCK_DATA.json') as f:
            self.mock_data = json.load(f)

    def test_add_facebook_accounts(self):
        for account in self.mock_data:
            fb_account = FacebookAccount(
                name=account['name'],
                email=account['email'],
                phone_number=account['phone_number'],
                password=account['password'],
                uid=account['uid'],
                cookie=account['cookie'],
                profile_picture=account['profile_picture']
            )
            fb_account.save()
            # Verify that the account was created
            self.assertEqual(FacebookAccount.objects.count(), self.mock_data.index(account) + 1)

    