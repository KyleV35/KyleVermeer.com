from google.appengine.ext import db
from datetime import date

import logging

class BrickBreaker(db.Model):
    top_score = db.IntegerProperty();
    name = db.StringProperty();