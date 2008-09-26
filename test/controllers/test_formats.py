import logging
import unittest

from webtest import TestApp

from controllers import test_helper

class TestControllerFormats(unittest.TestCase):
  
  def setUp(self):
    self.application = test_helper.get_application()
  
  def test_html(self):
    app = TestApp(self.application)
    response = app.get('/s3hub/')
    self.assertEqual('200 OK', response.status)
    # XXX: Actually test the data
    self.assertTrue('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">' in response)    
    
  def test_rss(self):
    app = TestApp(self.application)
    response = app.get('/s3hub/?format=rss')
    self.assertEqual('200 OK', response.status)
    # XXX: Actually test the data
    self.assertTrue('<?xml version="1.0" encoding="UTF-8"?>' in response)
    
  def test_json(self):
    app = TestApp(self.application)
    response = app.get('/s3hub/?format=json')
    self.assertEqual('200 OK', response.status)
    # XXX: Actually test the data
    self.assertTrue('"bucket": "s3hub"' in response)
    
  def test_xspf(self):
    app = TestApp(self.application)
    response = app.get('/m1xes/sub-pop-mix-1/?format=xspf')
    self.assertEqual('200 OK', response.status)
    # XXX: Actually test the data
    self.assertTrue('<playlist version="0" xmlns="http://xspf.org/ns/0/">' in response)
    
  def test_tape(self):
    app = TestApp(self.application)
    response = app.get('/m1xes/sub-pop-mix-1/?format=tape')
    self.assertEqual('200 OK', response.status)
    # XXX: Actually test the data
    self.assertTrue('<ul id="songs">' in response)
    
  def test_id3(self):
    app = TestApp(self.application)
    response = app.get('/m1xes/sub-pop-mix-1/01-Dntel-The_Distance_%28ft._Arthur%26Yu%29.mp3?format=id3-json')
    self.assertEqual('200 OK', response.status)
    # XXX: Actually test the data
    self.assertTrue('"title": "The Distance (Ft. Arthur & Yu)"' in response)