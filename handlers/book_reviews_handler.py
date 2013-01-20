import webapp2
import logging
import datetime
from urllib import unquote_plus
from handlers.base_handler import BaseHandler
from webapp2_extras import json
from models.familyMember import *
from google.appengine.ext import db
from google.appengine.api import memcache
from util.memcacheHelper import safeMemcacheSet
from util.template import jinja_environment
from models.games import BrickBreakerTopScore
from models.blog import BlogPost

class BookReviewHandler(BaseHandler):
    def get(self):
        template= jinja_environment.get_template('book_reviews/HTWF_Chapter1.html')
        self.response.out.write(template.render({}))