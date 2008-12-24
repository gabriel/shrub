import logging
import xml.sax
from xml.sax.handler import ContentHandler
import re
import iso8601

from shrub.file import S3File

class BucketContentHandler(ContentHandler):
  """Parses ListBucketResult response:
 
  <ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
    <Name>mus1c</Name>
    <Prefix></Prefix>
    <Marker></Marker>
    <MaxKeys>1000</MaxKeys>
    <NextMarker>somefile</NextMarker>
    <IsTruncated>false</IsTruncated>
    <Contents>
      <Key>01 Gabe&apos;s Mix Tape 2007-11-17.mp3</Key>
      <LastModified>2007-11-17T22:34:27.000Z</LastModified>
      <ETag>&quot;b034f4ff7eca12eefc2e5c2a207f45eb&quot;</ETag>
      <Size>67653780</Size>
      <StorageClass>STANDARD</StorageClass>
    </Contents>
    <Contents>...</Contents>
    <CommonPrefixes><Prefix>foo/bar</Prefix></CommonPrefixes>
  """

  def __init__(self, content=None):
    self.name = None
    self.marker = None
    self.next_marker = None
    self.is_truncated = False
    self.prefix = None
    self.max_keys = None  
    self.files = []
    self.prefixes = []
    self.dirs = set([])
    
    self.contents = []
    self.handler = None 
    
    if content:
      xml.sax.parseString(content, self)
      
  def __json__(self):
    return dict(name=self.name, prefix=self.prefix, maxKeys=self.max_keys, isTrucated=self.is_truncated, contents=self.files, commonPrefixes=self.prefixes)

  def startElement(self, name, attrs):
    if self.handler != None: 
      self.handler.startElement(name, attrs)
      return
    
    if name == 'Contents':
      self.handler = ObjectContentHandler(self.name, self.prefix)
    elif name == 'CommonPrefixes':
      self.handler = PrefixContentHandler(self.name, self.prefix)
    else:
      self.handler = None
      
    return None
  
  def characters(self, content):
    if self.handler != None: 
      self.handler.characters(content)
      return
    
    self.contents.append(content)
    
  def content(self):
    content = u''.join(self.contents)
    self.contents = []
    return content

  def endElement(self, name):
    
    content = self.content()
    
    if name == 'Contents':  
      file = self.handler.file    
      self.files.append(file)
      if file.is_folder: 
        self.dirs.add(file.name)
        
      self.handler = None
      return
    elif name == 'CommonPrefixes':
      for prefix in self.handler.prefixes:
        if not prefix.name in self.dirs:
          self.files.append(prefix)
          
      
    if self.handler != None: 
      self.handler.endElement(name)
      return
    
    if name == 'Name':
      self.name = content
    if name == 'IsTruncated':      
      self.is_truncated = content == 'true'
    elif name == 'Marker':
      self.marker = content
    elif name == 'NextMarker':
      self.next_marker = content
    elif name == 'Prefix':
      self.prefix = content
    elif name == 'MaxKeys':
      self.max_keys = content
        
class ObjectContentHandler(ContentHandler):
  
  def __init__(self, bucket_name, prefix):
    self.bucket_name = bucket_name
    self.prefix = prefix
    self.file = None
    self.contents = []
  
  def startElement(self, name, attrs): 
    return None
    
  def characters(self, content):
    self.contents.append(content)
  
  def content(self):
    content = u''.join(self.contents)
    self.contents = []
    return content
  
  def endElement(self, name): 
    
    content = self.content()
    
    if name == 'Key': 
      key = content
      self.file = S3File(self.bucket_name, key)
      
      is_folder = False
            
      if self.prefix and self.prefix.endswith('/'):
        self.file.name = re.sub(re.escape(self.prefix), '', key)      
      
      # Check if folder
      p = re.compile('_\$folder\$\Z')      
      if p.search(self.file.name):
        self.file.name = p.sub('', self.file.name) + "/"
        self.file.is_folder = True      
      
    elif name == 'ETag': 
      self.file.etag = content
    elif name == 'LastModified': 
      self.file.last_modified = iso8601.parse_date(content)
    elif name == 'Size': 
      self.file.size = long(content) 
    elif name == 'StorageClass': 
      self.file.storage_class = content

class PrefixContentHandler(ContentHandler):
  '''Handler for CommonPrefixes'''

  def __init__(self, bucket_name, prefix):
    self.bucket_name = bucket_name
    self.prefix = prefix
    self.prefixes = []
    self.contents = []

  def startElement(self, name, attrs): 
    return None

  def characters(self, content):
    self.contents.append(content)
    
  def content(self):
    content = u''.join(self.contents)
    self.contents = []
    return content

  def endElement(self, name): 
    
    content = self.content()

    if name == 'Prefix': 
      prefix_name = content
      if self.prefix and self.prefix.endswith('/'): 
        prefix_name = re.sub('\A%s' % self.prefix, '', prefix_name)
        
      file = S3File(self.bucket_name, prefix_name)
      file.is_folder = True
      self.prefixes.append(file)
