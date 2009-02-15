# !/usr/bin/env python
#
# Copyright 2008 Gabriel Handford
#

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