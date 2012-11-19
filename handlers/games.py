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
from models.games import BrickBreaker

class GamesPageHandler(BaseHandler):
    def get(self):
        template= jinja_environment.get_template('games.html')
        self.response.out.write(template.render({}))

class BrickBreakerPageHandler(BaseHandler):
    def get(self):
        BBDB = BrickBreaker.get_by_key_name("High_Score_DB")
        template_values = {
            "top_score": BBDB.top_score
        }
        template= jinja_environment.get_template('brick_breaker.html')
        self.response.out.write(template.render(template_values))
        
class BrickBreakerHighScoresHandler(BaseHandler):
    def get(self):
        BBDB = BrickBreaker.get_by_key_name("High_Score_DB");
        top_score = BBDB.top_score
        self.response.out.write(top_score)
    def post(self):
        BBDB = BrickBreaker.get_by_key_name("High_Score_DB");
        top_score = BBDB.top_score
        score = int(self.request.get("score"))
        name = self.request.get("name")
        if top_score < score:
            BBDB.top_score = score
            BBDB.name = name
            BBDB.put()
            self.response.out.write("You have set a new high score!")
        else:
            self.response.out.write("No new high score!")