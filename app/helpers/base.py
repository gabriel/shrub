import os
import simplejson

def current_version(context):
  return os.environ['CURRENT_VERSION_ID']

def to_json(context, value):
  return simplejson.dumps(value)
