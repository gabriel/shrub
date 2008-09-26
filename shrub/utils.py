import urllib
import os

def current_url():
  name = os.environ['SERVER_NAME']
  port = int(os.environ['SERVER_PORT'])
  
  if port == 80 or port == 443: return name    
  return '%s:%s' % (name, port)

class S3Utils:
  
  @staticmethod
  def params_to_url(params):
    pairs = ['%s=%s' % (key, value) for key, value in params.items()]
    paramString = '&'.join(pairs)
    if paramString: return paramString
    return ''
    
  @staticmethod
  def parse_request(request, prefix=None):
    request_path = urllib.unquote(request.path)    
    if prefix: 
      request_path = re.sub('%s$' % prefix, '', request_path)
    
    bucket_name = None
    prefix = None    
    
    if request_path != '/':
      paths = request_path.split('/')[1:]
      bucket_name = paths[0]
      prefix = '/'.join(paths[1:])
      #if prefix and not prefix.endswith('/'): prefix += '/'
      
    return bucket_name, prefix
  
  @staticmethod  
  def file_comparator(x, y, sort, sort_asc):
    # Change sort aliases
    if sort == "date": sort = "last_modified" 
    if sort == "name": sort = "key"

    a = b = None

    if sort == "key" or sort == "size" or sort == "last_modified":
      a = getattr(x, sort)
      b = getattr(y, sort)

    if a is None and b is not None: return 1
    elif a is not None and b is None: return -1
    elif a is None and b is None: return 0

    if isinstance(a, str): a = a.lower()
    if isinstance(b, str): b = b.lower()

    if sort_asc: return cmp(a, b)
    else: return cmp(b, a)