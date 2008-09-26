import urllib
import logging

from google.appengine.api import urlfetch

from shrub.response import S3BucketResponse, S3ErrorResponse
from shrub.utils import S3Utils

class S3:
  
  DefaultLocation = 's3.amazonaws.com'
  
  def list(self, bucket_name, max_keys, prefix, delimiter, marker):
    
    url_options = { }
    
    if max_keys: url_options['max-keys'] = str(max_keys)
    if prefix: url_options['prefix'] = urllib.quote(prefix, '')
    if delimiter: url_options['delimiter'] = urllib.quote(delimiter, '')
    if marker: url_options['marker'] = urllib.quote(marker, '')
    
    url = u'http://%s/%s?%s' % (S3.DefaultLocation, bucket_name, S3Utils.params_to_url(url_options))
    logging.info("URL: %s", url)
    
    try:
      response = urlfetch.fetch(url)
      return S3BucketResponse(url, int(response.status_code), response.content)
    except Exception, detail:
      logging.error('Error: %s' % detail)
      return S3ErrorResponse(url, 500, str(detail))
        

    
