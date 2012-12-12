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