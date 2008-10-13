from shrub.sax import BucketContentHandler

class S3HTTPResponse(object):
  
  def __init__(self, url, status_code):
    self.url = url
    self.status_code = status_code
    
  def ok(self):
    return (self.status_code >= 200 and self.status_code <= 299)
  ok = property(ok)


class S3Response(S3HTTPResponse):
  
  def __init__(self, class_, url, status_code, content=None):
    super(S3Response, self).__init__(url, status_code)
    self.content = class_(content)
    self.message = None
    
  @property
  def path_components(self):
    bucket_name = self.content.name
    prefix = self.content.prefix    
        
    dirs = [ bucket_name ]
    if prefix: 
      dirs += prefix.split("/")[:-1]
      
    return dirs
    
  @property
  def path(self):
    return u'/'.join(self.path_components)
    
            
class S3ErrorResponse(S3HTTPResponse):
  
  def __init__(self, url, status_code, message):
    super(S3ErrorResponse, self).__init__(url, status_code)
    self.message = message
    
  def __str__(self):
    return self.message
    
    
class S3BucketResponse(S3Response):
  
  def __init__(self, url, status_code, content=None):
    super(S3BucketResponse, self).__init__(BucketContentHandler, url, status_code, content)
    
    self.is_truncated = self.content.is_truncated
    self.max_keys = self.content.max_keys
    self.files = self.content.files
  

