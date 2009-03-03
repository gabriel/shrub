
class Track:
	'''Track in an XSPF feed'''
	
	def __init__(self, location, meta, title, info):
		self.location = location
		self.meta = meta
		self.title = title
		self.info = info
		
	def __str__(self):
		return 'location=%s,meta=%s,title=%s,info=%s' % (self.location, self.meta, self.title, self.info)

