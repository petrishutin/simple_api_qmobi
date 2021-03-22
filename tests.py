import json
import os
import time
import unittest
import subprocess
from urllib import request


class TestServerResponce(unittest.TestCase):

    @classmethod
    def setUp(cls):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, "main.py")
        cls.server = subprocess.Popen(path)
        time.sleep(0.5)
        cls.response = request.urlopen('http://0.0.0.0:8080/')

    @classmethod
    def tearDown(cls):
        cls.server.kill()

    def test_server_root_200(self):
        self.assertEqual(self.response.status, 200)

    def test_server_json_payload(self):
        payload = self.response.read().decode()
        data = json.loads(payload)
        self.assertIn('exchange_rates', data)
        self.assertEqual(len(data['exchange_rates']), 2)


if __name__ == '__main__':
    unittest.main()
