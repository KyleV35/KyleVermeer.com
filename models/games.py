from google.appengine.ext import db
from datetime import date

import logging

class BrickBreakerTopScore(db.Model):
    score = db.IntegerProperty();
    name = db.StringProperty();