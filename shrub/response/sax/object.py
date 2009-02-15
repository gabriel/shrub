import logging
import xml.sax
from xml.sax.handler import ContentHandler
import re
import iso8601

from shrub.file import S3File

class ObjectParser(ContentHandler):

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

