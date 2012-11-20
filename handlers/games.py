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
import json

class GamesPageHandler(BaseHandler):
    def get(self):
        template= jinja_environment.get_template('games.html')
        self.response.out.write(template.render({}))

class BrickBreakerPageHandler(BaseHandler):
    def get(self):
        template_values= get_top_5_scores()
        template= jinja_environment.get_template('brick_breaker.html')
        self.response.out.write(template.render(template_values))
        
class BrickBreakerHighScoresHandler(BaseHandler):
    def post(self):
        score = int(self.request.get("score"))
        name = self.request.get("name")
        sort_score(score,name)
        
        self.response.out.write(json.dumps(get_top_5_scores()))
            
class BrickBreakerInitHandler(BaseHandler):
    def get(self):
        top_score_1 = BrickBreakerTopScore(key_name="High_Score_DB_1",score=0, name="None")
        top_score_1.put()
        top_score_2 = BrickBreakerTopScore(key_name="High_Score_DB_2",score=0, name="None")
        top_score_2.put()
        top_score_3 = BrickBreakerTopScore(key_name="High_Score_DB_3",score=0, name="None")
        top_score_3.put()
        top_score_4 = BrickBreakerTopScore(key_name="High_Score_DB_4",score=0, name="None")
        top_score_4.put()
        top_score_5 = BrickBreakerTopScore(key_name="High_Score_DB_5",score=0, name="None")
        top_score_5.put()
        
def sort_score(score,name):
    score,name = swap_out_top_score_1(score,name)
    score,name = swap_out_top_score_2(score,name)
    score,name = swap_out_top_score_3(score,name)
    score,name = swap_out_top_score_4(score,name)
    score,name = swap_out_top_score_5(score,name)
        
def swap_out_top_score_1(score,name):
    top_score_1_db = BrickBreakerTopScore.get_by_key_name("High_Score_DB_1")
    if (score >= top_score_1_db.score):
        temp_score = top_score_1_db.score
        temp_name = top_score_1_db.name
        top_score_1_db.score = score
        top_score_1_db.name = name
        top_score_1_db.put()
        return temp_score,temp_name
    else:
        return score,name
    
def swap_out_top_score_2(score,name):
    top_score_2_db = BrickBreakerTopScore.get_by_key_name("High_Score_DB_2")
    if (score >= top_score_2_db.score):
        temp_score = top_score_2_db.score
        temp_name = top_score_2_db.name
        top_score_2_db.score = score
        top_score_2_db.name = name
        top_score_2_db.put()
        return temp_score,temp_name
    else:
        return score,name
    
def swap_out_top_score_3(score,name):
    top_score_3_db = BrickBreakerTopScore.get_by_key_name("High_Score_DB_3")
    if (score >= top_score_3_db.score):
        temp_score = top_score_3_db.score
        temp_name = top_score_3_db.name
        top_score_3_db.score = score
        top_score_3_db.name = name
        top_score_3_db.put()
        return temp_score,temp_name
    else:
        return score,name
    
def swap_out_top_score_4(score,name):
    top_score_4_db = BrickBreakerTopScore.get_by_key_name("High_Score_DB_4")
    if (score >= top_score_4_db.score):
        temp_score = top_score_4_db.score
        temp_name = top_score_4_db.name
        top_score_4_db.score = score
        top_score_4_db.name = name
        top_score_4_db.put()
        return temp_score,temp_name
    else:
        return score,name
    
def swap_out_top_score_5(score,name):
    top_score_5_db = BrickBreakerTopScore.get_by_key_name("High_Score_DB_5")
    if (score >= top_score_5_db.score):
        temp_score = top_score_5_db.score
        temp_name = top_score_5_db.name
        top_score_5_db.score = score
        top_score_5_db.name = name
        top_score_5_db.put()
        return temp_score,temp_name
    else:
        return score,name
        
def get_top_5_scores():
    BBDB_1 = BrickBreakerTopScore.get_by_key_name("High_Score_DB_1")
    BBDB_2 = BrickBreakerTopScore.get_by_key_name("High_Score_DB_2")
    BBDB_3 = BrickBreakerTopScore.get_by_key_name("High_Score_DB_3")
    BBDB_4 = BrickBreakerTopScore.get_by_key_name("High_Score_DB_4")
    BBDB_5 = BrickBreakerTopScore.get_by_key_name("High_Score_DB_5")
    template_values = {
        "top_score_1_DB": {
            "score": BBDB_1.score,
            "name": BBDB_1.name
        },
        "top_score_2_DB": {
            "score": BBDB_2.score,
            "name": BBDB_2.name
        },
        "top_score_3_DB": {
            "score": BBDB_3.score,
            "name":BBDB_3.name
        },
        "top_score_4_DB": {
            "score": BBDB_4.score,
            "name": BBDB_4.name
        },
        "top_score_5_DB": {
            "score": BBDB_5.score,
            "name": BBDB_5.name
        }
    }
    return template_values;
