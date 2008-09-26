import urllib
import re

import shrub.feeds.rss
import shrub.feeds.xspf

import shrub.utils

class S3File:
  
  DefaultLocation = 's3.amazonaws.com'
  DefaultContentType = 'application/octet-stream'

  def __init__(self, bucket=None, key=None):
    self.id = u'%s/%s' % (bucket, key)
    self.bucket = bucket    
    self.key = key
    self.name = key
    self.metadata = {}
    self.content_type = self.DefaultContentType
    self.filename = None
    self.etag = None
    self.last_modified = None
    self.owner = None
    self.storage_class = None
    self.size = None
    self.is_folder = False
    
    self.pretty_last_modified_cache = None
    self.pretty_size_cache = None
  
  def __hash__(self):
    return self.id.__hash__()
    
  def __eq__(self, other):
    return self.id.__eq__(other.id)
    
  def __str__(self):
    return u'%s/%s' % (self.bucket, self.key)
  
  def __json__(self):
    return dict(bucket=self.bucket, key=self.key, etag=self.etag, lastModified=self.last_modified, size=self.size, storageClass=self.storage_class)
    
  def name_with_prefix(self, prefix):
    if prefix:
      if prefix.endswith('/'): return prefix + self.name
      else: return "%s/%s" % (prefix, self.name)
    
    return self.name    
    
  def pretty_last_modified(self, default):
    if not self.last_modified: return default    
    if not self.pretty_last_modified_cache: self.pretty_last_modified_cache = self.last_modified.strftime("%b %d, %Y, %I:%M %p")      
    return self.pretty_last_modified_cache
    
  def __pretty_size(self, size):
    if size == 0: return "-"
    suffixes = [("B",2**10), ("K",2**20), ("M",2**30), ("G",2**40), ("T",2**50)]
    for suf, lim in suffixes:
      if size > lim:
        continue
      else:
        return round(size/float(lim/2**10),2).__str__()+suf
    
  def pretty_size(self, default):
    if not self.size: return default    
    if not self.pretty_size_cache: self.pretty_size_cache = self.__pretty_size(self.size)
    return self.pretty_size_cache
    
  def name_without_extension(self):
    position = self.name.rfind('.')
    if position == -1: return self.name
    return self.name[0:position]
    
  def extension(self):
    position = self.name.rfind('.')
    if position == -1: return
    return self.name[position + 1:]    
  
  def to_appspot_url(self):
    if self.is_folder:
      name = re.sub(re.escape('_\$folder\$\Z'), '/', self.key)      
    else:
      name = self.key
    
    return u'http://%s/%s/%s' % (shrub.utils.current_url(), urllib.quote(self.bucket.encode('utf-8')), urllib.quote(name))
      
  def to_url(self, secure):
    scheme = 'http';
    if secure: scheme = 'https'    
    return u'%s://%s/%s/%s' % (scheme, self.DefaultLocation, urllib.quote(self.bucket.encode('utf-8')), urllib.quote(self.key.encode('utf-8')))
  
  def to_rss_item(self):
    link = self.to_url(False)
    if self.is_folder:
      link = self.to_appspot_url()
      
    description = None
    if not self.is_folder:
      #description = ' &nbsp; <a href="%s">Download</a>' % self.to_url(False)
      description = ''
      pretty_size = self.pretty_size(None)
      if pretty_size: description += 'Size: %sb' % pretty_size      
    
    return shrub.feeds.rss.Item(self.name, None, description, pub_date=self.last_modified, guid=link)
    
  def to_xspf_track(self):
    return shrub.feeds.xspf.Track(location=self.to_url(False), meta=self.extension(), title=self.name_without_extension(), info=None)