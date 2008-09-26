
from app.controllers.s3 import DefaultPage, S3Page
from google.appengine.ext import webapp

def get_application():
  return webapp.WSGIApplication([('/', DefaultPage),('/.*', S3Page)], debug=True)
    