from google.appengine.ext import db
from datetime import date

class BlogPost(db.Model):
    """Models a blog post"""
    author = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    title = db.StringProperty()
    body= db.TextProperty()