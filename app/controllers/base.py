import os
import logging
import re

from google.appengine.ext import webapp
from google.appengine.api import memcache

from mako import exceptions
from mako.template import Template
from mako.lookup import TemplateLookup

import simplejson

import shrub


class PrintEnvironmentHandler(webapp.RequestHandler):
	def get(self):
		for name in os.environ.keys():
			self.response.out.write("%s = %s<br />\n" % (name, os.environ[name]))


class BasePage(webapp.RequestHandler):
	"""Base request handler to provide template lookup and rendering"""
	
	def __init__(self):
		super(BasePage, self).__init__()
		self._template_lookup = None
		
	def view_path(self):
		return os.path.join(os.path.dirname(__file__), "..", "views")
		
	@property
	def template_lookup(self):
		if not self._template_lookup:
			self._template_lookup = TemplateLookup(directories=[self.view_path()] + shrub.view_paths(), output_encoding='utf-8')
		return self._template_lookup
		
	def get_template(self, name):
		return self.template_lookup.get_template(name)
		
	def set_content_type(self, content_type):
		self.response.headers['Content-Type'] = content_type
		
	def render(self, name, values, content_type=None, cache_key=None):
		template = self.get_template(name)
		if content_type:
			self.set_content_type(content_type)
			
		try:
			self.render_text(template.render(**values), cache_key=cache_key)
		except:
			self.render_text(exceptions.html_error_template().render())
			
	def render_text(self, text, cache_key=None):
		if cache_key:
		# Cache for 5 minutes
			memcache.add(cache_key, text, 5 * 60)
			
		self.response.out.write(text)
		
	def render_with_cache(self, cache_key, content_type=None):
		data = memcache.get(cache_key)
		if data is not None:
			if content_type: self.set_content_type(content_type)
			self.render_text(data)
			return True
		return False


class BaseResponse(object):
	"""Base response when using a front controller"""
	
	def __init__(self, request_handler):
		self.request_handler = request_handler
		self.request = request_handler.request
		
	def render(self, name, values, content_type=None, cache_key=None):
		self.request_handler.render(name, values, content_type=content_type, cache_key=cache_key)


class JSONResponse(BaseResponse):

	ContentType = "text/javascript; charset=utf-8"
	
	def _wrap_in_callback(self, data, callback):
	
	# Callback function names may only use upper and lowercase alphabetic characters (A-Z, a-z),
	# numbers (0-9), the period (.), the underscore (_)
	
		if not re.match("^[a-zA-Z0-9._]+$", callback):
			raise shrub.ShrubException("InvalidCallback", "Callback contains invalid characters")
			
		return "%s(%s)" % (callback, data)
		
	def render_json(self, value, cache_key=None, callback=None):
		json = simplejson.dumps(value)
		self.request_handler.set_content_type(self.ContentType)
		if callback:
			json = self._wrap_in_callback(json, callback)
		self.request_handler.render_text(json, cache_key=cache_key)
		
	def render_json_from_cache(self, cache_key):
		return self.request_handler.render_with_cache(cache_key, content_type=self.ContentType)

	def render_json_error(self, status_code, error):
		self.request_handler.response.set_status(status_code)
		self.render_json(dict(error=dict(code=error.code, message=error.message)))
		
	def handle(self, response):
		callback = self.request.get("callback", None)
		try:
			self.render_json(response, callback=callback)
		except shrub.ShrubException, e:
			self.render_json_error(500, e)
			

