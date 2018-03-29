import hive_handler
import aiohttp
import unittest
import json
import requests

import time


class EndpointTestCase(unittest.TestCase):
  def test_auth(self):
    result = requests.get(base_url + 'users')
    self.assertEqual(result.status_code, 401, msg='did not get a 401')

  def test_empty(self):
    result = requests.get(base_url + 'users', headers={'access-token': '12345678'})
    self.assertEqual(result.json(), [], msg='result was not empty')

  def test_target_user(self):
    hive_handler.cursor.execute('INSERT INTO TABLE target_users select 42')

    result = requests.get(base_url + 'target_users', headers={'access-token': '12345678'})
    self.assertDictEqual(result.json()[0], {'user_id': 42})


time.sleep(3)
unittest.main()
