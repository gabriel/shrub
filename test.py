# !/usr/bin/env python
#
# Copyright 2008 Gabriel Handford
#
"""
Tests:

To run the tests, load the dev_server and go to: 

  http://localhost:8080/test?package=controllers
  
"""

import sys
import os
import logging
sys.path = [ 
  os.path.join(os.path.dirname(__file__), "lib"), 
  os.path.join(os.path.dirname(__file__), "test"),
  os.path.join(os.path.dirname(__file__), "test", "lib") ] + sys.path

import gaeunit

if __name__ == '__main__':
  gaeunit.main()