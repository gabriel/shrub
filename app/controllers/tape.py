import logging

from google.appengine.api import urlfetch

from id3 import id3reader
from id3 import id3data

from shrub.utils import S3Utils
from app.controllers.base import BaseResponse

class TapeResponse(BaseResponse):
  
  def __init__(self, request_handler):
    self.request_handler = request_handler

  def handle(self, s3response):
    
    list_url = self.request_handler.request.path_url
    xspf_url = '%s?format=xspf' % list_url
    
    tracks = []
    id3_urls = []
    for file in s3response.files:
      if file.extension() == 'mp3':
        tracks.append(file.to_xspf_track())
        id3_urls.append('%s?format=id3-json' % file.to_appspot_url())
          
    values = dict(title='Mix Tape (%s)' % s3response.path(), xspf_url=xspf_url, list_url=list_url, tracks=tracks, id3_urls=id3_urls)
    
    self.render("muxtape.mako", values)
    
    
class XSPFResponse(BaseResponse):
  
  def handle(self, s3response):    
    url = s3response.url
    files = s3response.files
    path = s3response.path()
    
    files.sort(cmp=lambda x, y: S3Utils.file_comparator(x, y, 'name', True))
    
    tracks = []
    
    for file in files:
      tracks.append(file.to_xspf_track())      
      
    title = u'%s (XSPF)' % path
    
    values = dict(title=title, creator='Shrub', info='http://shrub.appspot.com', location=url, tracks=tracks)
  
    self.render("xspf.mako", values, 'text/xml;charset=utf-8')
    
    
class ID3Response(BaseResponse):
  
  def load_url(self, url, format='json', cache_key=None):
    
    if self.request_handler.render_json_with_cache(cache_key):
      return
    
    logging.info("Loading url: %s" % url)
    fetch_headers = dict(Range='bytes=0-1024') 
    response = urlfetch.fetch(url, headers=fetch_headers, allow_truncated=True)
    
    try:
      data = id3data.ID3Data(response.content)
      id3r = id3reader.Reader(data, only_v2=True) 
      
      if not id3r.found:
        self.render_json(dict(error='Not found'))
        return
            
      values = dict(album=id3r.getValue('album'),
        performer=id3r.getValue('performer'),
        title=id3r.getValue('title'),
        track=id3r.getValue('track'),
        year=id3r.getValue('year'),
        isTruncated=id3r.is_truncated,
      )

      if format == 'json':        
        self.render_json(values, cache_key=cache_key)
        
    except id3reader.Id3Error, detail:
      self.render_json(dict(error=str(detail)))
    
    