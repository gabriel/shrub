
class Track:
  '''Track in an XSPF feed'''
  
  def __init__(self, location, meta, title, info):    
    self.location = location
    self.meta = meta
    self.title = title
    self.info = info