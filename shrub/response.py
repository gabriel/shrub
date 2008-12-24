from shrub.sax import BucketContentHandler

class S3HTTPResponse(object):
  
  def __init__(self, url, status_code):
    self.url = url
    self.status_code = status_code
    
  @property
  def ok(self):
    return (self.status_code >= 200 and self.status_code <= 299)


class S3Response(S3HTTPResponse):
  
  def __init__(self, parser_class, url, status_code, content=None, try_count=None, times=None):
    super(S3Response, self).__init__(url, status_code)
    self.data = parser_class(content)
    self.message = None
    self.try_count = try_count
    self.times = times
    
  @property
  def path_components(self):
    bucket_name = self.data.name
    prefix = self.data.prefix    
        
    dirs = [ bucket_name ]
    if prefix: 
      dirs += prefix.split("/")[:-1]
      
    return dirs
    
  @property
  def path(self):
    return u'/'.join(self.path_components)
  
  @property
  def total_time(self):
    if self.times is None: return None
    return reduce(lambda x, y: x+y, self.times)
            
class S3ErrorResponse(S3HTTPResponse):
  
  def __init__(self, url, status_code, message, **kwargs):
    super(S3ErrorResponse, self).__init__(url, status_code, **kwargs)
    self.message = message
    
  def __str__(self):
    return self.message
    
    
class S3BucketResponse(S3Response):
  
  def __init__(self, url, status_code, content, **kwargs):
    super(S3BucketResponse, self).__init__(BucketContentHandler, url, status_code, content, **kwargs)
    
    self.is_truncated = self.data.is_truncated
    self.max_keys = self.data.max_keys
    self.files = self.data.files

