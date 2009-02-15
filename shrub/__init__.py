import os

def view_paths():
	"""View path for views in this library."""
	return [os.path.join(os.path.dirname(__file__), "views")]


class ShrubException(Exception):

	def __init__(self, code, message):
		super(Exception, self).__init__()
		self.code = code
		self.message = message
