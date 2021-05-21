import responses
import json

from .helpers import mock_file, ClientTestCase


class TestClientPayment(ClientTestCase):

    def setUp(self):
        super(TestClientPayment, self).setUp()
        self.base_url = '{}/payments'.format(self.base_url)

    @responses.activate
    def test_payment_all(self):
        result = mock_file('payment_collection')
        url = self.base_url
        responses.add(responses.GET, url, status=200,
                      body=json.dumps(result), match_querystring=True)
        self.assertEqual(self.client.payment.all(), result)

    @responses.activate
    def test_payment_all_with_options(self):
        count = 1
        result = mock_file('payment_collection_with_one_payment')
        url = '{}?count={}'.format(self.base_url, count)
        responses.add(responses.GET, url, status=200, body=json.dumps(result),
                      match_querystring=True)
        self.assertEqual(self.client.payment.all({'count': count}), result)

    @responses.activate
    def test_payment_fetch(self):
        result = mock_file('fake_payment')
        url = '{}/{}'.format(self.base_url, self.payment_id)
        responses.add(responses.GET, url, status=200, body=json.dumps(result),
                      match_querystring=True)
        self.assertEqual(self.client.payment.fetch('fake_payment_id'), result)

    @responses.activate
    def test_payment_capture(self):
        result = mock_file('fake_captured_payment')
        url = '{}/{}/capture'.format(self.base_url, self.payment_id)
        responses.add(responses.POST, url, status=200,
                      body=json.dumps(result), match_querystring=True)
        self.assertEqual(self.client.payment.capture(self.payment_id,
                                                     amount=5100), result)

    @responses.activate
    def test_refund_create(self):
        result = mock_file('fake_refund')
        url = '{}/{}/refund'.format(self.base_url, self.payment_id)
        responses.add(responses.POST, url, status=200, body=json.dumps(result),
                      match_querystring=True)
        self.assertEqual(self.client.payment.refund(self.payment_id, 2000),
                         result)

    @responses.activate
    def test_transfer(self):
        param = {
            'transfers': {
                'currency': {
                    'amount': 100,
                    'currency': 'INR',
                    'account': 'dummy_acc'
                }
            }
        }
        result = mock_file('transfers_collection_with_payment_id')
        url = '{}/{}/transfers'.format(self.base_url, self.payment_id)
        responses.add(responses.POST, url, status=200, body=json.dumps(result),
                      match_querystring=True)
        self.assertEqual(self.client.payment.transfer(self.payment_id, param),
                         result)

    @responses.activate
    def test_transfer_fetch(self):
        result = mock_file('transfers_collection_with_payment_id')
        url = '{}/{}/transfers'.format(self.base_url, self.payment_id)
        responses.add(responses.GET, url, status=200, body=json.dumps(result),
                      match_querystring=True)
        self.assertEqual(self.client.payment.transfers(self.payment_id), result)

    @responses.activate
    def test_bank_transfer_fetch(self):
        result = mock_file('fake_bank_transfer')
        url = '{}/{}/bank_transfer'.format(self.base_url, self.payment_id)
        responses.add(responses.GET,
                      url,
                      status=200,
                      body=result,
                      match_querystring=True)

        response = self.client.payment.bank_transfer(self.payment_id)
        self.assertEqual(response['virtual_account_id'], 'va_8J2ny4Naokqbpe')
        self.assertEqual(response['payment_id'], self.payment_id)
