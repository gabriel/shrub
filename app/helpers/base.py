import os
import simplejson

def current_version(context):
  return os.environ.get('CURRENT_VERSION_ID','Unknown')

def to_json(context, value):
  return simplejson.dumps(value)
