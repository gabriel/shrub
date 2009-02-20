import urllib
import cgi
import re

def html_escape(string):
	return cgi.escape(string, True)

def url_escape(string, plus=True):
	# convert into a list of octets
	string = string.encode("utf8")
	return urllib.quote_plus(string) if plus else urllib.quote(string)

def url_unescape(string):
	text = urllib.unquote_plus(string)
	if not is_ascii_str(text):
		text = text.decode("utf8")
	return text

_ASCII_re = re.compile(r'\A[\x00-\x7f]*\Z')

def is_ascii_str(text):
	return isinstance(text, str) and _ASCII_re.match(text)

def params_to_url(params, urlescape=False):
	def maybe_escape(s):
		return url_escape(s) if urlescape else s
	pairs = ['%s=%s' % (maybe_escape(key), maybe_escape(value)) for key, value in params.items() if key is not None and value is not None]
	return '&'.join(pairs)

def file_comparator(x, y, sort, sort_asc):
	# Change sort aliases
	if sort == "date": sort = "last_modified"
	if sort == "name": sort = "key"

	a = b = None

	if sort == "key" or sort == "size" or sort == "last_modified":
		a = getattr(x, sort)
		b = getattr(y, sort)

	if a is None and b is not None: return 1
	elif a is not None and b is None: return -1
	elif a is None and b is None: return 0

	if isinstance(a, str): a = a.lower()
	if isinstance(b, str): b = b.lower()

	if sort_asc: return cmp(a, b)
	else: return cmp(b, a)
