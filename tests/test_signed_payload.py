from tests.test_case import TestCase
from eth_keys import keys
import json
import base64

class TestApi(TestCase):
    def print_payload_signature(self):
        pk = keys.PrivateKey(b'\x01' * 32)

        payload = {
            "service_proposal": {
                "id": 1,
                "format": "service-proposal/v1",
                "provider_id": "node1",
            }
        }

        signature = pk.sign_msg(json.dumps(payload))
        print json.dumps(payload)
        print pk.public_key.to_checksum_address().lower()
        print base64.b64encode(signature.to_bytes())


    def test_signed_payload(self):
        payload = {
            "service_proposal": {
                "id": 1,
                "format": "service-proposal/v1",
                "provider_id": "node1",
            }
        }

        headers = {
            "identity": "0x1a642f0e3c3af545e7acbd38b07251b3990914f1",
            "Authorization": "Signature Da1mAwK5abmXQCNsCE+YjsZbR9jTyEKqdrjxxMKwNzwr2NFnM35UiVQJWcg8rgL+X2PR60LoIUMlGU9OPaSoZwE="
        }

        re = self.client.post(
            '/v1/signed_payload',
            data=json.dumps(payload),
            headers=headers
        )

        self.assertEqual({}, re.json)
        self.assertEqual(200, re.status_code)


    def test_incorrectly_signed_payload(self):
        payload = {}

        headers = {
            "identity": "0x0000000000000000000000000000000000000001",
            "Authorization": "Signature Da1mAwK5abmXQCNsCE+YjsZbR9jTyEKqdrjxxMKwNzwr2NFnM35UiVQJWcg8rgL+X2PR60LoIUMlGU9OPaSoZwE="
        }

        re = self.client.post(
            '/v1/signed_payload',
            data=json.dumps(payload),
            headers=headers
        )

        self.assertEqual({'error': 'payload was not signed with provided identity'}, re.json)
        self.assertEqual(401, re.status_code)


    def test_incorrectly_authentication_type(self):
            headers = {
                "Authorization": "Basic Da1mAwK5abmXQCNsCE+YjsZbR9jTyEKqdrjxxMKwNzwr2NFnM35UiVQJWcg8rgL+X2PR60LoIUMlGU9OPaSoZwE="
            }

            re = self.client.post(
                '/v1/signed_payload',
                data=json.dumps({}),
                headers=headers
            )

            self.assertEqual({'error': 'authentication type have to be Signature'}, re.json)
            self.assertEqual(401, re.status_code)