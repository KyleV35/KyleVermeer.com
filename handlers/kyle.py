import webapp2
import logging
import datetime
from handlers.base_handler import BaseHandler
from webapp2_extras import json
from models.familyMember import *
from google.appengine.ext import db
from google.appengine.api import memcache
from util.memcacheHelper import safeMemcacheSet
from util.template import jinja_environment
from models.games import BrickBreakerTopScore

class FrontPageHandler(BaseHandler):
    def get(self):
        template= jinja_environment.get_template('front_page.html')
        self.response.out.write(template.render({}))
        
class KyleExamplesHandler(BaseHandler):
    def get(self):
        template= jinja_environment.get_template('kyle_examples.html')
        self.response.out.write(template.render({}))
        
class ContactPageHandler(BaseHandler):
    def get(self):
        template= jinja_environment.get_template('contact.html')
        self.response.out.write(template.render({}))
        
class SaraPageHandler(BaseHandler):
    def get(self):
        template= jinja_environment.get_template('sara.html')
        self.response.out.write(template.render({}))
        
class AboutPageHandler(BaseHandler):
    def get(self):
        template= jinja_environment.get_template('about.html')
        self.response.out.write(template.render({}))