from google.appengine.ext import db
from datetime import date
import re
import logging

class BlogPost(db.Model):
    """Models a blog post"""
    author = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    title = db.StringProperty()
    body= db.TextProperty()
    previous = db.SelfReferenceProperty(collection_name="previous_set")
    next = db.SelfReferenceProperty(collection_name="next_set")
    @db.ComputedProperty
    def year(self):
        return self.date.year
    @db.ComputedProperty
    def month(self):
        return self.date.month
    @db.ComputedProperty
    def day(self):
        return self.date.day
    
    def get_formatted_date(self):
        unformatted_date= self.date
        day= unformatted_date.day
        month = unformatted_date.month
        year = unformatted_date.year
        return str(month) + "/" + str(day) + "/" + str(year)
        
    def get_body_html(self):
        body_html = ""
        sentances = self.body.split('\n')
        for s in sentances:
            if s.strip() != '':
                logging.info(s)
                body_html = body_html + '<p>' + s+'</p>'
        #body_html = body_html + self.body.replace('\n','</p><p>')
        #body_html = body_html + "</p>"
        logging.info(body_html)
        return body_html
        
    @staticmethod
    def get_most_recent():
        return BlogPost.all().order('-date').get()