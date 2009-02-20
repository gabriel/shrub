import os
from shrub.utils import url_unescape
import logging

def current_gae_url():
	name = os.environ['SERVER_NAME']
	port = int(os.environ['SERVER_PORT'])
	
	if port == 80 or port == 443: return name
	return '%s:%s' % (name, port)

def parse_gae_request(request, prefix=None):
	"""Parse bucket name and prefix from gae request."""
	request_path = url_unescape(request.path)
	logging.info('request_path=%s (%s)' % (request_path, request.path))
	if prefix:
		request_path = re.sub('%s$' % prefix, '', request_path)

	bucket_name = None
	prefix = None

	if request_path != '/':
		paths = request_path.split('/')[1:]
		bucket_name = paths[0]
		prefix = '/'.join(paths[1:])

	return bucket_name, prefix