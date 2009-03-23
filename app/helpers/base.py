import os
import simplejson

def current_version(context):
	return str(os.environ.get('CURRENT_VERSION_ID', 'Unknown'))
	
def to_json(context, value):
	return simplejson.dumps(value)

def shrub_version(context):
	return "1.2.10"