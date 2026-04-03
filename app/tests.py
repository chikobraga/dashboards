from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from app.models import Account, InfoPossession, PossessionTitle, TitleAttr, Transactions


class DashboardViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='secret123')
        self.account_1 = Account.objects.create(
            accountnumber=1001,
            name='Alice',
            balance='100.00',
            user=self.user,
        )
        self.account_2 = Account.objects.create(
            accountnumber=1002,
            name='Bob',
            balance='50.00',
        )
        self.title = PossessionTitle.objects.create(
            numberid=1,
            name_title='Avenida Central',
            owner_title=self.account_1,
            color='1',
            value='80.00',
        )
        TitleAttr.objects.create(
            possession=self.title,
            name_attr='Casa',
            value='20.00',
            type_info='1',
        )
        self.info = InfoPossession.objects.create(
            description='Hotel',
            value='40.00',
            info_possession=self.title,
            type_info='2',
        )
        self.api_client = APIClient()

    def test_login_redirects_to_account_page(self):
        response = self.client.post(
            '/',
            {'username': 'alice', 'password': 'secret123'},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'account/1001/')

    def test_account_page_loads(self):
        response = self.client.get('/account/1001/')

        self.assertEqual(response.status_code, 200)

    def test_transaction_api_creates_two_transactions_and_updates_balances(self):
        response = self.api_client.post(
            '/api/transaction/',
            {
                'transaction': 'W',
                'update_account': self.account_1.pk,
                'dest_account': self.account_2.pk,
                'value': '25.00',
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.account_1.refresh_from_db()
        self.account_2.refresh_from_db()
        self.assertEqual(self.account_1.balance, Decimal('75.00'))
        self.assertEqual(self.account_2.balance, Decimal('75.00'))
        self.assertEqual(Transactions.objects.count(), 2)

    def test_info_possession_api_uses_correct_resource(self):
        response = self.api_client.get(f'/api/infop/{self.info.pk}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['description'], 'Hotel')
