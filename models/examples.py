from google.appengine.ext import db
from datatime import date

class Example(db.Model):
    title = db.StringProperty()
    description = db.TextProperty()
    blurb = db.StringProperty()
    blurb_image_location = db.StringProperty()
    link = db.LinkProperty()
