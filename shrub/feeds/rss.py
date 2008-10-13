import rfc822
import time

class Item:
  '''Item in an RSS feed'''
  
  def __init__(self, title, link, description=None, pub_date=None, guid=None):
    self.title = title
    self.link = link
    self.description = description
    self.pub_date = pub_date
    self.guid = guid
  
  @property
  def rfc822_pub_date(self):
    return rfc822.formatdate(time.mktime(self.pub_date.timetuple()))