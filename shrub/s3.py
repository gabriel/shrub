from __future__ import with_statement
import urllib
import logging

from google.appengine.api import urlfetch

from shrub.response import S3BucketResponse, S3ErrorResponse
from shrub.utils import S3Utils

class S3:
  
  DefaultLocation = 's3.amazonaws.com'
  
  def _fetch(self, url, retry_count, **kwargs):
    """Calls urlfetch.fetch with retry count"""
    try_count = 0
    while try_count < retry_count:
      try:
        try_count += 1
        response = urlfetch.fetch(url, **kwargs)
        # Retry on 5xx errors as well as urlfetch exceptions
        if int(response.status_code) in range(500, 600):
          continue
        return response
      except Exception, error:
        logging.error('Error(%s): %s' % (try_count, error))
        if try_count >= retry_count:
          raise
  
  def list(self, bucket_name, max_keys, prefix, delimiter, marker, cache=60, retry_count=3):
    if retry_count < 0: raise ValueError, "Invalid retry_count < 0"
    
    url_options = { }
    
    if max_keys: url_options['max-keys'] = str(max_keys)
    if prefix: url_options['prefix'] = urllib.quote(prefix, '')
    if delimiter: url_options['delimiter'] = urllib.quote(delimiter, '')
    if marker: url_options['marker'] = urllib.quote(marker, '')
    
    url = u'http://%s/%s?%s' % (S3.DefaultLocation, bucket_name, S3Utils.params_to_url(url_options))
    logging.info("URL: %s", url)
    
    headers = {'Cache-Control':'max-age=%s' % cache}
    try:
      response = self._fetch(url, retry_count, headers=headers)
      return S3BucketResponse(url, int(response.status_code), response.content)
    except Exception, error:
      return S3ErrorResponse(url, 503, str(error))
