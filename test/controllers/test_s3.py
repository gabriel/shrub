import logging
import unittest

from controllers import test_helper
from webtest import TestApp

class TestS3(unittest.TestCase):
  
  def setUp(self):
    self.application = test_helper.get_application()
  
  def test_home(self):
    app = TestApp(self.application)
    response = app.get('/')
    self.assertEqual('200 OK', response.status)
    self.assertTrue('Amazon S3 Proxy' in response)  