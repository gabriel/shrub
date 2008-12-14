import os
import logging
import urllib
import cgi
import datetime

from google.appengine.ext import webapp
from google.appengine.runtime import DeadlineExceededError

from mako.template import Template
from mako.lookup import TemplateLookup

from shrub.utils import S3Utils
from shrub.s3 import S3

from app.controllers.base import BasePage, BaseResponse
from app.controllers.tape import TapeResponse, XSPFResponse, ID3Response

from shrub import feeds

class DefaultPage(BasePage):
  """Home page"""

  def get(self):
    search = self.request.get('q')
    if search:
      self.redirect("/" + search)
      return

    self.render("index.mako", dict(title="Shrub / Amazon S3 Proxy"))

class S3Page(BasePage):
  """
  Front controller for all S3 style requests (until I figure out how to do more advanced routing). 
  
  Request should be passed off based on their format or response type.
  """
  
  def _get(self):  
    max_keys = self.request.get('max-keys')
    delimiter = self.request.get('delimiter', '/')
    marker = self.request.get('marker')    
    format = self.request.get('format', None)
    
    cache_key = self.request.url
    
    bucket_name, prefix = S3Utils.parse_request(self.request)    
    
    if not bucket_name:
      handler = ErrorResponse(self)
      handler.render_error(404)
      return
    
    if format == 'id3-json':
      url = 'http://%s/%s' % (S3.DefaultLocation, self.request.path)
      ID3Response(self).load_url(url, 'json', cache_key=cache_key)
      return
        
    # Make S3 request
    s3response = S3().list(bucket_name, max_keys, prefix, delimiter, marker)        
      
    # If not 2xx, show friendly error page
    if not s3response.ok:
      handler = ErrorResponse(self)
      handler.handle(s3response)
      return
        
    # If no format use HTML response
    if not format:
      handler = HTMLResponse(self)          
      handler.handle(s3response)
      return

    # If truncated with a request format; return 501
    if s3response.is_truncated:
      handler = ErrorResponse(self)
      handler.render_error(501, "There were too many items ( &gt; %s ) in the current bucket to display. The results were truncated and may be inaccurate." % s3_response.max_keys)
      return
    
    # Get handler for format
    if format == 'rss': handler = RSSResponse(self)
    elif format == 'xspf': handler = XSPFResponse(self)
    elif format == 'tape': handler = TapeResponse(self)
    elif format == 'json': handler = JSONResponse(self)
    else:
      # If no handler for a format return error page
      handler = ErrorResponse(self)
      handler.render_error(404, "The requested format parameter is unknown.", title="Not found")
      return
        
    if handler: handler.handle(s3response)

  def get(self):
    try:
      self._get()
    except DeadlineExceededError:
      self.response.clear()
      ErrorResponse(self).render_error(500, "The request couldn't be completed in time. Please try again.")
      
      

class ErrorResponse(BaseResponse):
  """Handle standard error response."""
  
  def __init__(self, request_handler):
    self.request_handler = request_handler
    
  def render_error(self, status_code, error_message=None, title="Error"):    
    self.request_handler.response.set_status(status_code)
    self.request_handler.render("error.mako", dict(title=title, s3url=None, status_code=status_code, message=error_message, path=None))
  
  def handle(self, s3response):
    title = None
    message = None
    url = s3response.url
    request = self.request_handler.request
    
    status_code = s3response.status_code
    error_message = s3response.message
    
    if status_code == 403:
      title = 'Permission denied'
      message = 'Shrub does not have permission to access this bucket. Shrub can only act on public buckets.'
    elif status_code == 404:
      title = 'Not found'
      message = 'This bucket or folder was not found. Try verifying that it exists.'
    elif status_code in range(400, 500):
      title = 'Client error'
      message = 'There was an error trying to access S3.'
    elif status_code in range(500, 600):
      title = 'Not available. Please try again.'
      message = 'There was an error trying to access S3. Please try again.' 
    else:
      title = 'Unknown error'
      message = 'There was an unknown error.'
      
    if error_message:
      message += ' (%s)' % error_message
        
    self.request_handler.response.set_status(status_code)
    self.request_handler.render("error.mako", dict(title=title, s3url=url, status_code=status_code, message=message, request=request))
      

class HTMLResponse(BaseResponse):
  
  def handle(self, s3response):        
    files = s3response.files
    path_components = s3response.path_components
    path = s3response.path

    # Sort files
    sort = self.request.get('s', 'name')
    sort_asc = True    
    if sort.endswith('-desc'): 
      sort = sort.replace('-desc', '', 1)
      sort_asc = False    
    
    files.sort(cmp=lambda x, y: S3Utils.file_comparator(x, y, sort, sort_asc))
  
    # Render response
    template_values = {
      'title': path,
      'path_components': path_components,
      'path': path,
      'sort': sort,
      'sort_asc': sort_asc,
      's3response': s3response
    }
  
    self.render("list.mako", template_values)

class JSONResponse(BaseResponse):

  def handle(self, s3response):
    self.render_json(s3response.content)
    
class RSSResponse(BaseResponse):

  def handle(self, s3response):    
    files = s3response.files
    path = s3response.path

    rss_items = []
    files.sort(cmp=lambda x, y: S3Utils.file_comparator(x, y, 'date', False))

    for file in files[:50]:
      rss_items.append(file.to_rss_item())

    pub_date = datetime.datetime.now()
    if len(rss_items) > 0:
      pub_date = rss_items[0].pub_date

    title = u'%s (Shrub)' % path
    link = "http://s3hub.appspot.com/%s" % path

    assigns = dict(title=title, description=u'RSS feed for %s' % s3response.url, items=rss_items, link=link, pub_date=pub_date)
    self.render("rss.mako", assigns, 'text/xml;charset=utf-8')