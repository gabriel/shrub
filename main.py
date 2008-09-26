# !/usr/bin/env python
#
# Copyright 2008 Gabriel Handford
#
"""Shrub: Amazon S3 Proxy (http://shrub.appspot.com)"""

__author__ = "Gabriel Handford"
__email__ = "gabrielh@gmail.com"
__copyright__= "Copyright (c) 2008, Gabriel Handford"
__license__ = "MIT"
__url__ = "http://shrub.appspot.com"

import sys
import os
import logging
sys.path = [ os.path.join(os.path.dirname(__file__), "lib") ] + sys.path

import re
import datetime
import wsgiref.handlers

from google.appengine.ext import webapp

from app.controllers.s3 import DefaultPage, S3Page

def main():
  application = webapp.WSGIApplication([
    ('/', DefaultPage),
    ('/.*', S3Page),
    ], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
