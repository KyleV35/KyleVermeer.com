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
from models.blog import BlogPost

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
        
class WhatsUpHandler(BaseHandler):
    def get(self):
        template= jinja_environment.get_template('examples/whats_up.html')
        self.response.out.write(template.render({}))
        
class NewBlogPostHandler(BaseHandler):
    def get(self):
        template= jinja_environment.get_template('create_blog_post.html')
        self.response.out.write(template.render({}))
        
    def post(self):
        #Check referer to prevent CSRF
        if self.request.referer != "http://www.kylevermeer.com/blog/create_new":
            return webapp2.redirect('/about')
        title = self.request.get("title") 
        author = self.request.get("author")
        body = self.request.get("body")
        password = self.request.get("password")
        
        #Check password
        if password != "betsy says post":
            return webapp2.redirect('/blog')
            
        
        blog_post_number_query = BlogPost.all(keys_only=True)
        num_blog_posts = blog_post_number_query.count()
        new_blog_post_num = str(num_blog_posts+1)
        new_key_name = "BlogPost" + new_blog_post_num
        
        #Find last blog post to set up linked list
        last_blog_post = BlogPost.get_by_key_name("BlogPost"+str(num_blog_posts))
        new_blog_post = BlogPost(author=author,title=title,body=body, key_name= new_key_name)
        
        #If this is first blog post
        if last_blog_post is None:
            new_blog_post.next = None
        else :
            last_blog_post.previous = new_blog_post.key()
            last_blog_post.put()
            new_blog_post.next = last_blog_post.key()
        new_blog_post.previous = None
        new_blog_post.put()
        self.response.out.write("")
        return webapp2.redirect('/blog')
        
class BlogHandlerLatest(BaseHandler):
    def get(self):
        self.response.out.write(create_blog_post_response())
        
class BlogHandler(BaseHandler):
    def get(self,year,month,day):
        self.response.out.write(create_blog_post_response(year,month,day))
        
        
def create_blog_post_response(year = None,month = None,day = None):
    blog_post_query = BlogPost.all().order('-date')
    if year is not None:
        blog_post_query.filter('year =',long(year))
        blog_post_query.filter('month =',long(month))
        blog_post_query.filter('day =',long(day))
    blog_post = blog_post_query.get()
    template_values = {
        "blog_post" : blog_post
    }
    template= jinja_environment.get_template('blog.html')
    return template.render(template_values)