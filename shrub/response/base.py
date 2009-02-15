from shrub.response.sax.bucket import BucketParser

class S3BaseResponse(object):

	def __init__(self, url, status_code, try_count=None, times=None):
		self.url = url
		self.status_code = status_code
		self.try_count = try_count
		self.times = times

	@property
	def ok(self):
		return (self.status_code >= 200 and self.status_code <= 299)


class S3Response(S3BaseResponse):

	def __init__(self, parser_class, url, status_code, content=None, **kwargs):
		super(S3Response, self).__init__(url, status_code, **kwargs)
		self.parser_class = parser_class
		self.content = content
		self.message = None
		self._data = None

	@property
	def path_components(self):
		bucket_name = self.data.name
		prefix = self.data.prefix
		
		dirs = [ bucket_name ]
		if prefix:
			dirs += prefix.split("/")[:-1]
			
		return dirs

	@property
	def path(self):
		return u'/'.join(self.path_components)

	@property
	def total_time(self):
		if self.times is None: return None
		return reduce(lambda x, y: x+y, self.times)

	@property
	def data(self):
		if not self._data:
			self._data = self.parser_class(self.content)
		return self._data


class S3ErrorResponse(S3BaseResponse):

	def __init__(self, url, status_code, message, **kwargs):
		super(S3ErrorResponse, self).__init__(url, status_code, **kwargs)
		self.message = message
		
	def __str__(self):
		return self.message


class S3BucketResponse(S3Response):

	def __init__(self, url, status_code, content, **kwargs):
		super(S3BucketResponse, self).__init__(BucketParser, url, status_code, content, **kwargs)

		self.is_truncated = self.data.is_truncated
		self.max_keys = self.data.max_keys
		self.files = self.data.files
		self.next_marker = None
		if self.is_truncated:
			self.next_marker = self.data.next_marker