from __future__ import with_statement
import urllib
import logging
from datetime import datetime

from google.appengine.api import urlfetch

from shrub.response.base import S3BucketResponse, S3ErrorResponse
import shrub.utils

class S3:

	DefaultLocation = 's3.amazonaws.com'

	def _fetch(self, url, retry_count, **kwargs):
		"""Calls urlfetch.fetch with retry count"""
		try_count = 0
		times = []
		response = None
		while try_count < retry_count:
			try:
				try_count += 1

				# Fetch the url
				fetch_start = datetime.now()
				response = urlfetch.fetch(url, **kwargs)
				times.append(datetime.now() - fetch_start)

				# TODO(gabe): Handle PermanentRedirect error messages (no Location header on 301 so need to handle manually)

				# Retry on 5xx errors as well as urlfetch exceptions
				if int(response.status_code) in xrange(500, 600):
					continue

				return response, try_count, times

			except Exception, error:
				logging.error('Error(%s): %s' % (try_count, error))
				if try_count >= retry_count:
					raise
		return response, try_count, times

	def list(self, bucket_name, max_keys=None, prefix=None, delimiter=None, marker=None, cache=60, retry_count=3):
		if retry_count < 0: raise ValueError, "Invalid retry_count < 0"

		url_options = dict(prefix=prefix, delimiter=delimiter, marker=marker)
		if max_keys: url_options['max-keys'] = str(max_keys)

		# Use http://bucketname.s3.amazonaws.com, instead of http://s3.amazonaws.com/bucketname
		url = u'http://%s.%s/?%s' % (bucket_name, S3.DefaultLocation, shrub.utils.params_to_url(url_options, True))
		logging.info("URL: %s", url)

		headers = {'Cache-Control':'max-age=%s' % (cache)}
		try:
			response, try_count, times = self._fetch(url, retry_count, headers=headers)
			return S3BucketResponse(url, int(response.status_code), response.content, try_count=try_count, times=times)
		except Exception, error:
			# TODO(gabe): Need to disable this in debug mode, so exceptions raise properly
			return S3ErrorResponse(url, 503, str(error))

