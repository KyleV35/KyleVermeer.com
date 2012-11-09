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

class FamilyMainPageHandler(BaseHandler):
    def get(self):
        template = jinja_environment.get_template('family_main.html')
        self.response.out.write(template.render({}))

class FamilyHandler(BaseHandler):
    def get(self,familyMemberName):
        familyMember= getFamilyMember(familyMemberName)
        profile_video= getVideo(familyMember.profile_video)
        template_values= {
            'familyMember':familyMember,
            'video':profile_video,
        }
        template = jinja_environment.get_template('family.html')
        self.response.out.write(template.render(template_values))
        
class VideoHandler(BaseHandler):
    def get(self):
        name= self.request.get("name")
        familyMember= getFamilyMember(name)
        videos= familyMember.get_videos()
        template_values= {
            'familyMember':familyMember,
            'videos':videos
        }
        template= jinja_environment.get_template('videos.html')
        self.response.out.write(template.render(template_values))
        
class VideoLikeHandler(BaseHandler):
    def get(self):
        videoID= self.request.get("videoID")
        video = getVideo(videoID)
        video.addLike()
    def post(self):
        videoID= self.request.get("videoID")
        video = getVideo(videoID)
        video.addLike()
        likes= video.likes
        json_response= json.encode(value=likes)
        self.response.out.write(json_response)
                
class DummyData(BaseHandler):
    def get(self):
        createGrant()
        createPaige()
        self.response.out.write("Success!")
        
def getFamilyMember(name):
    familyMember= memcache.get(name)
    if familyMember is not None:
        return familyMember
    else:
        q= db.Query(FamilyMember)
        q.filter('normalized_name =',name.lower())
        familyMember= q.get()
        safeMemcacheSet(name,familyMember)
        return familyMember
    
def getVideo(key):
    if key is not None:
        video= memcache.get(key)
        if video is not None:
            return video
        else:
            video= Video.get_by_key_name(key)
            memcache.add(key,video)
            return video
    else:
        return None
        
def createGrant():
    grant= FamilyMember(key_name="grant",first_name="Grant",last_name="Vermeer")
    grant.normalized_name= "grant"
    grant.birth_date= datetime.date(1995,5,8) # May 8, 1995
    grant.high_school= 'Bellarmine College Preparatory'
    grant.email= db.Email('boovermeer@gmail.com')
    grant.profile_picture= "Grant_Vermeer.png"
    grant.profile_video= "PJ35W910WQ4"
    grant.height= "6'3\""
    grant.weight= "185"
    grant.high_school_link= "http://www.bcp.org/athletics/team_basketball.aspx"
    grant.name_image_string= 'GrantVermeerName2.png'
    grant.GPA= "4.4"
    grant.twitter_username= "GrantVermeer21"
    safeMemcacheSet(key=grant.normalized_name,value=grant)
    createVideosGrant(grant)
    grant.put()
    
def createPaige():
    paige= FamilyMember(key_name="paige",first_name="Paige",last_name="Vermeer")
    paige.normalized_name= "paige"
    paige.birth_date= datetime.date(1997,8,5) # August 5, 1997
    paige.high_school= 'Castilleja School'
    paige.high_school_link= "http://www.castillejabasketball.com"
    paige.email= db.Email('paigevermeer@gmail.com')
    paige.profile_picture= "Paige_Vermeer.png"
    paige.height= "5'7\""
    paige.weight= None
    paige.name_image_string= 'PaigeVermeerName.png'
    paige.GPA= "3.8"
    safeMemcacheSet(key=paige.normalized_name,value=paige)
    paige.put()
    
def createVideosGrant(grant):
    makeVideo(videoID="PJ35W910WQ4",family_member=grant,video_name="Grant Vermeer Kills the City of Champions Tournament")
    makeVideo(videoID="6x_gL61feeU",family_member=grant,video_name="Grant Vermeer Gerry Freitas Showcase 2012 CCSF Day 1")
    makeVideo(videoID="TD6wtwihxsc",family_member=grant,video_name="Grant \"Boo\" Vermeer 2011-12 Highlights")
    makeVideo(videoID="-sBMQhW3v0I",family_member=grant,video_name="Grant \"Boo\" Vermeer - Sophomore Varsity Season 2010-11")
    
def makeVideo(videoID,family_member,video_name):
    video= Video(key_name=videoID, family_member=family_member,likes=0, youtube_id=videoID, parent=family_member)
    video.video_name= video_name 
    video.put()
    safeMemcacheSet(key=videoID,value=video)
    
    