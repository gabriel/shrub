import re, iso8601, traceback, logging
import xml.sax
from xml.sax.handler import ContentHandler, ErrorHandler



from shrub.file import S3File

from shrub.response.sax.object import ObjectParser

class Parser(ContentHandler):
	pass
	
class BucketParser(Parser):
	"""
	SAX parser for ListBucketResult response.
	
  <ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
    <Name>stuff</Name>
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
		<CommonPrefixes><Prefix>foo/baz</Prefix></CommonPrefixes>"""
	
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
		
		try:
			xml.sax.parseString(content, self)
		except:
			logging.info('Error parsing response: %s' % traceback.format_exc())
			raise
			
	def __json__(self):
		return dict(name=self.name, prefix=self.prefix, maxKeys=self.max_keys, isTrucated=self.is_truncated, contents=self.files, commonPrefixes=self.prefixes)
		
	def startElement(self, name, attrs):
		if self.handler != None:
			self.handler.startElement(name, attrs)
			return
			
		if name == 'Contents':
			self.handler = ObjectParser(self.name, self.prefix)
		elif name == 'CommonPrefixes':
			self.handler = PrefixesParser(self.name, self.prefix)
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
					
			self.handler = None
			return
			
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


class PrefixesParser(Parser):
	'''SAX parser for CommonPrefixes'''
	
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
				prefix_name = re.sub('\A%s' % re.escape(self.prefix), '', prefix_name)
				
			file = S3File(self.bucket_name, prefix_name)
			file.is_folder = True
			self.prefixes.append(file)

