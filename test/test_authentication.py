from datetime import datetime, timedelta
from unittest import TestCase
from abl.util import sign, verify


class AuthenticationTests(TestCase):

    def test_signature(self):
        params = {'foo': 'bar', 'spam': 3}
        secret = 'SuperSecretSecret'
        signed_params = sign(params, secret)
        self.assertTrue(verify(signed_params, secret))

    def test_invalid_signature(self):
        params = {'foo': 'bar', 'spam': 3}
        secret = 'SuperSecretSecret'
        signed_params = sign(params, secret)
        signed_params['signature'] = 'superinvalid'
        self.assertFalse(verify(signed_params, secret))

    def test_missing_signature(self):
        params = {'foo': 'bar', 'spam': 3}
        secret = 'SuperSecretSecret'
        signed_params = sign(params, secret)
        del signed_params['signature']
        self.assertFalse(verify(signed_params, secret))

    def test_invalid_timestamp(self):
        params = {'foo': 'bar', 'spam': 3}
        secret = 'SuperSecretSecret'
        signed_params = sign(params, secret)
        signed_params["timestamp"] = "foo"
        self.assertFalse(verify(signed_params, secret))

    def test_missing_timestamp(self):
        params = {'foo': 'bar', 'spam': 3}
        secret = 'SuperSecretSecret'
        signed_params = sign(params, secret)
        del signed_params["timestamp"]
        self.assertFalse(verify(signed_params, secret))

    def test_timestamp_too_old(self):
        params = {'foo': 'bar', 'spam': 3}
        secret = 'SuperSecretSecret'
        signed_params = sign(params, secret)
        signed_params["timestamp"] = (datetime.utcnow() - timedelta(hours=3)).strftime("%s.%f")
        self.assertFalse(verify(signed_params, secret))

    def test_timestamp_in_future(self):
        params = {'foo': 'bar', 'spam': 3}
        secret = 'SuperSecretSecret'
        signed_params = sign(params, secret)
        signed_params["timestamp"] = (datetime.utcnow() + timedelta(hours=3)).strftime("%s.%f")
        self.assertFalse(verify(signed_params, secret))
